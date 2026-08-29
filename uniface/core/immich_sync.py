import os
import sys
import json
import shutil
import hashlib
import configparser
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from uniface.core.config import ROOT_DIR
from uniface.core.logging import get_logger

logger = get_logger(__name__)

# Standard clean import with fallback for local repo
try:
    import immich_sdk
    from immich_sdk import Configuration, ApiClient
    from immich_sdk.api import assets_api, albums_api, tags_api, users_api, people_api, search_api
    from immich_sdk.models import (
        CreateAlbumDto, TagCreateDto, BulkIdsDto, TagBulkAssetsDto,
        MetadataSearchDto
    )
except ImportError:
    _sdk_path = str(ROOT_DIR / "immich_sdk_repo")
    if os.path.exists(_sdk_path) and _sdk_path not in sys.path:
        sys.path.insert(0, _sdk_path)
    import immich_sdk
    from immich_sdk import Configuration, ApiClient
    from immich_sdk.api import assets_api, albums_api, tags_api, users_api, people_api, search_api
    from immich_sdk.models import (
        CreateAlbumDto, TagCreateDto, BulkIdsDto, TagBulkAssetsDto,
        MetadataSearchDto
    )

def _get_configuration(url: str, api_key: str) -> Configuration:
    base_url = url.rstrip("/")
    if base_url.endswith("/api"):
        base_url = base_url[:-4]
    
    configuration = Configuration(host=f"{base_url}/api")
    configuration.api_key['x-api-key'] = api_key
    configuration.api_key['api_key'] = api_key
    return configuration

def _normalize_base_url(url: str) -> str:
    base_url = url.rstrip("/")
    if base_url.endswith("/api"):
        base_url = base_url[:-4]
    return base_url

def _get_ini_immich_local_path() -> str:
    """Read local_path from uni-face.ini [IMMICH] section."""
    try:
        ini_path = os.path.join(ROOT_DIR, "uni-face.ini")
        if os.path.exists(ini_path):
            config = configparser.ConfigParser()
            config.read(ini_path, encoding="utf-8")
            if config.has_section("IMMICH"):
                return config.get("IMMICH", "local_path", fallback="").strip()
    except Exception as e:
        logger.debug(f"Failed to read ini immich local_path: {e}")
    return ""

def _resolve_local_immich_path(original_path: Optional[str], user_local_path: Optional[str] = None) -> Optional[str]:
    """
    Translates Immich container original_path (e.g. upload/library/admin/IMG.jpg or /usr/src/app/upload/...)
    to the host filesystem path if configured via user_local_path or uni-face.ini.
    """
    if not original_path:
        return None
        
    # 1. Check if original_path already exists directly on host
    if os.path.exists(original_path):
        return os.path.abspath(original_path)
        
    # 2. Get local storage directory from WebUI parameter or uni-face.ini fallback
    local_path = (user_local_path or "").strip() or _get_ini_immich_local_path()
    if not local_path or not os.path.exists(local_path):
        return None
        
    local_path = os.path.abspath(local_path)
    norm_orig = original_path.replace("\\", "/")
    
    # 3. Check direct concatenation
    c1 = os.path.join(local_path, norm_orig.lstrip("/"))
    if os.path.exists(c1):
        return c1
        
    # 4. Check stripping common container upload/library prefixes
    for marker in ["/upload/", "upload/", "/library/", "library/"]:
        if marker in norm_orig:
            subpath = norm_orig.split(marker, 1)[1]
            c2 = os.path.join(local_path, subpath)
            if os.path.exists(c2):
                return c2
            if "library" in marker:
                c3 = os.path.join(local_path, "library", subpath)
                if os.path.exists(c3):
                    return c3
            elif "upload" in marker:
                c4 = os.path.join(local_path, "upload", subpath)
                if os.path.exists(c4):
                    return c4
                    
    # 5. Fallback: match filename in local directory tree
    base_name = os.path.basename(original_path)
    for root, _, files in os.walk(local_path):
        if base_name in files:
            found = os.path.join(root, base_name)
            if os.path.exists(found):
                return found
                
    return None

def test_immich_connection(url: str, api_key: str) -> Dict[str, Any]:
    """
    Test Immich server connection and authentication.
    """
    base_url = _normalize_base_url(url)
    try:
        req = urllib.request.Request(f"{base_url}/api/users/me", headers={"x-api-key": api_key, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            name = data.get("name", "User")
            return {"success": True, "message": f"Connected as {name}"}
    except Exception as e:
        logger.error(f"Immich connection test failed: {e}")
        return {"success": False, "message": f"Connection Failed: {str(e)}"}

def get_immich_albums_list(url: str, api_key: str) -> Dict[str, Any]:
    """
    Retrieve all albums from Immich.
    """
    base_url = _normalize_base_url(url)
    try:
        req = urllib.request.Request(f"{base_url}/api/albums", headers={"x-api-key": api_key, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            
        albums_list = data if isinstance(data, list) else data.get("albums", [])
        album_dicts = [
            {
                "id": a.get("id"), 
                "name": a.get("albumName") or a.get("name") or "Unnamed Album",
                "assetCount": a.get("assetCount", len(a.get("assets", [])))
            } 
            for a in albums_list
        ]
        return {"success": True, "albums": album_dicts}
    except Exception as e:
        logger.error(f"Failed to fetch Immich albums: {e}")
        return {"success": False, "message": str(e), "albums": []}

def get_immich_tags_list(url: str, api_key: str) -> Dict[str, Any]:
    """
    Retrieve all tags from Immich.
    """
    base_url = _normalize_base_url(url)
    try:
        req = urllib.request.Request(f"{base_url}/api/tags", headers={"x-api-key": api_key, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            
        tags_list = data if isinstance(data, list) else data.get("tags", [])
        tag_dicts = [{"id": t.get("id"), "name": t.get("name")} for t in tags_list]
        return {"success": True, "tags": tag_dicts}
    except Exception as e:
        logger.error(f"Failed to fetch Immich tags: {e}")
        return {"success": False, "message": str(e), "tags": []}

def get_immich_people_list(url: str, api_key: str) -> Dict[str, Any]:
    """
    Retrieve named people from Immich (excludes unnamed faces).
    """
    base_url = _normalize_base_url(url)
    try:
        target = f"{base_url}/api/people?withHidden=false"
        req = urllib.request.Request(target, headers={"x-api-key": api_key, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
            
        people_list = raw.get("people", raw) if isinstance(raw, dict) else raw
        if not isinstance(people_list, list):
            people_list = getattr(raw, "people", []) if hasattr(raw, "people") else []

        named_people = []
        for p in people_list:
            if isinstance(p, dict):
                p_id = str(p.get("id", ""))
                name = (p.get("name") or "").strip()
                thumb = p.get("thumbnailPath") or p.get("thumbnail_path") or ""
            else:
                p_id = str(getattr(p, "id", ""))
                name = (getattr(p, "name", None) or "").strip()
                thumb = getattr(p, "thumbnail_path", "") or getattr(p, "thumbnailPath", "")

            if name:
                named_people.append({
                    "id": p_id,
                    "name": name,
                    "thumbnailPath": thumb
                })
        return {"success": True, "people": named_people}
    except Exception as e:
        logger.error(f"Failed to fetch Immich people: {e}", exc_info=True)
        return {"success": False, "message": str(e), "people": []}

def _fetch_all_search_metadata(base_url: str, api_key: str, filter_dict: dict) -> list:
    """
    Fetch all pages of assets matching filter_dict from /api/search/metadata without 1000 limit.
    """
    all_items = []
    page = 1
    page_size = 1000
    while True:
        body = {**filter_dict, "size": page_size, "page": page}
        payload = json.dumps(body).encode("utf-8")
        try:
            req = urllib.request.Request(
                f"{base_url}/api/search/metadata",
                data=payload,
                headers={"x-api-key": api_key, "Content-Type": "application/json", "Accept": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=20.0) as resp:
                search_res = json.loads(resp.read().decode("utf-8"))
                items = []
                if isinstance(search_res, dict) and "assets" in search_res:
                    items = search_res["assets"].get("items", [])
                elif isinstance(search_res, list):
                    items = search_res
                
                if not items:
                    break
                all_items.extend(items)
                if len(items) < page_size:
                    break
                page += 1
                if page > 100: # Safety cap 100,000 items
                    break
        except Exception as e:
            logger.warning(f"Error fetching search/metadata page {page}: {e}")
            break
            
    return all_items

def _parse_asset_model(item: Any, base_url: str) -> Dict[str, Any]:
    if isinstance(item, dict):
        asset_id = str(item.get("id", ""))
        orig_name = str(item.get("originalFileName") or item.get("original_file_name") or item.get("originalPath") or f"{asset_id}.jpg")
        media_type = str(item.get("type", "IMAGE")).lower()
        duration = item.get("duration")
        original_path = item.get("originalPath") or item.get("original_path")
    else:
        asset_id = str(getattr(item, "id", "") or "")
        orig_name = str(getattr(item, "original_file_name", "") or getattr(item, "original_path", "") or f"{asset_id}.jpg")
        m_type = getattr(item, "type", "IMAGE")
        media_type = str(getattr(m_type, "value", m_type) if hasattr(m_type, "value") else m_type).lower()
        duration = getattr(item, "duration", None)
        original_path = getattr(item, "original_path", None)

    duration_sec = None
    if duration:
        try:
            parts = str(duration).split(":")
            if len(parts) == 3:
                duration_sec = int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
            elif len(parts) == 2:
                duration_sec = int(parts[0]) * 60 + float(parts[1])
            else:
                duration_sec = float(duration)
        except Exception:
            pass

    return {
        "id": asset_id,
        "filename": os.path.basename(orig_name),
        "type": "video" if "video" in media_type else "image",
        "duration": duration_sec,
        "originalPath": original_path,
        "thumbnailUrl": f"/api/v1/immich/thumbnail/asset/{asset_id}"
    }

def get_immich_category_assets(
    url: str, 
    api_key: str, 
    category_type: str, 
    category_id: str
) -> Dict[str, Any]:
    """
    Retrieve asset list belonging to a specific Person, Album, or Tag with automatic pagination.
    """
    base_url = _normalize_base_url(url)
    try:
        assets_raw = []
        
        if category_type == "people":
            assets_raw = _fetch_all_search_metadata(base_url, api_key, {"personIds": [category_id]})
            if not assets_raw:
                try:
                    req = urllib.request.Request(f"{base_url}/api/people/{category_id}", headers={"x-api-key": api_key, "Accept": "application/json"})
                    with urllib.request.urlopen(req, timeout=10.0) as resp:
                        p_info = json.loads(resp.read().decode("utf-8"))
                        assets_raw = p_info.get("assets", [])
                except Exception as pe:
                    logger.warning(f"fallback GET /api/people/{category_id} failed: {pe}")

        elif category_type == "albums":
            try:
                req = urllib.request.Request(f"{base_url}/api/albums/{category_id}", headers={"x-api-key": api_key, "Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=20.0) as resp:
                    album_info = json.loads(resp.read().decode("utf-8"))
                    if isinstance(album_info, dict):
                        assets_raw = album_info.get("assets", []) or album_info.get("items", []) or album_info.get("albumAssets", [])
                    elif isinstance(album_info, list):
                        assets_raw = album_info
            except Exception as ae:
                logger.warning(f"GET /albums/{category_id} failed: {ae}")

            if not assets_raw:
                assets_raw = _fetch_all_search_metadata(base_url, api_key, {"albumIds": [category_id]})

        elif category_type == "tags":
            assets_raw = _fetch_all_search_metadata(base_url, api_key, {"tagIds": [category_id]})

        parsed_assets = []
        for item in assets_raw:
            parsed_assets.append(_parse_asset_model(item, base_url))
            
        return {"success": True, "assets": parsed_assets}
    except Exception as e:
        logger.error(f"Failed to fetch Immich category assets ({category_type}:{category_id}): {e}", exc_info=True)
        return {"success": False, "message": str(e), "assets": []}

def import_immich_assets(
    url: str, 
    api_key: str, 
    asset_ids: List[str], 
    target_dir: str,
    user_local_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Import selected Immich assets into local target_dir via Hardlink or Stream Download
    with Path Mapping and Hash Deduplication.
    """
    config = _get_configuration(url, api_key)
    base_url = _normalize_base_url(url)
    os.makedirs(target_dir, exist_ok=True)
    
    imported_files = []
    failed = []
    hardlink_count = 0
    download_count = 0
    copy_count = 0
    skipped_count = 0
    
    logger.info(f"--- START IMMICH ASSETS IMPORT --- (Count: {len(asset_ids)}, LocalPath: {user_local_path or 'auto'})")
    
    with ApiClient(config) as api_client:
        asset_api = assets_api.AssetsApi(api_client)
        
        for asset_id in asset_ids:
            try:
                info = asset_api.get_asset_info(id=asset_id)
                original_path = getattr(info, "original_path", None)
                fname = getattr(info, "original_file_name", None) or os.path.basename(original_path or f"{asset_id}.jpg")
                resolved_local = _resolve_local_immich_path(original_path, user_local_path)
                
                # Check for duplicate by content hash or deterministic filename
                base_name, ext = os.path.splitext(fname)
                if resolved_local and os.path.exists(resolved_local):
                    try:
                        with open(resolved_local, "rb") as f:
                            file_hash = hashlib.md5(f.read(65536)).hexdigest()[:10]
                        dst_filename = f"{base_name}_{file_hash}{ext}"
                    except Exception:
                        dst_filename = f"{base_name}_{asset_id[:8]}{ext}"
                else:
                    dst_filename = f"{base_name}_{asset_id[:8]}{ext}"
                
                dst_path = os.path.join(target_dir, dst_filename)
                
                # Deduplication check: if dst_path exists with non-zero size, reuse existing file
                if os.path.exists(dst_path) and os.path.getsize(dst_path) > 0:
                    skipped_count += 1
                    logger.debug(f"Skipping duplicate Immich asset: {dst_filename}")
                    imported_files.append({
                        "filename": dst_filename,
                        "file_id": f"immich/{dst_filename}",
                        "url": f"/workspace/uploads/immich/{dst_filename}",
                        "duration": getattr(info, "duration", None)
                    })
                    continue
                
                # Check if local hardlink/copy is possible
                linked = False
                if resolved_local and os.path.exists(resolved_local):
                    try:
                        os.link(resolved_local, dst_path)
                        linked = True
                        hardlink_count += 1
                        logger.debug(f"Hardlinked {resolved_local} -> {dst_path}")
                    except Exception as le:
                        try:
                            shutil.copy2(resolved_local, dst_path)
                            linked = True
                            copy_count += 1
                            logger.debug(f"Copied {resolved_local} -> {dst_path} (Hardlink error: {le})")
                        except Exception as ce:
                            logger.warning(f"Local file access failed: {ce}")
                
                # Fallback to HTTP download
                if not linked:
                    download_url = f"{base_url}/api/assets/{asset_id}/original"
                    req = urllib.request.Request(download_url, headers={"x-api-key": api_key})
                    with urllib.request.urlopen(req, timeout=30.0) as resp, open(dst_path, "wb") as out_file:
                        shutil.copyfileobj(resp, out_file)
                    download_count += 1
                    logger.debug(f"Downloaded asset {asset_id} -> {dst_path}")
                
                imported_files.append({
                    "filename": dst_filename,
                    "file_id": f"immich/{dst_filename}",
                    "url": f"/workspace/uploads/immich/{dst_filename}",
                    "duration": getattr(info, "duration", None)
                })
            except Exception as e:
                logger.error(f"Failed to import asset {asset_id}: {e}")
                failed.append({"id": asset_id, "error": str(e)})

    if hardlink_count > 0 and download_count == 0:
        method = "hardlink"
        skip_msg = f", {skipped_count} cached" if skipped_count > 0 else ""
        msg = f"⚡ Instant Hardlink: Imported {len(imported_files)} assets (0 MB used{skip_msg})"
    elif download_count > 0 and hardlink_count == 0:
        method = "download"
        skip_msg = f" ({skipped_count} cached)" if skipped_count > 0 else ""
        msg = f"☁️ Downloaded {len(imported_files)} assets from Immich Server{skip_msg}"
    else:
        method = "mixed"
        msg = f"Imported {len(imported_files)} assets ({hardlink_count} hardlinks, {download_count} downloads, {skipped_count} cached)"

    logger.info(f"--- END IMMICH IMPORT (Success: {len(imported_files)}, Hardlink: {hardlink_count}, Download: {download_count}, Cached: {skipped_count}, Failed: {len(failed)}) ---")
    return {
        "success": len(imported_files) > 0,
        "imported": imported_files,
        "failed": failed,
        "hardlink_count": hardlink_count,
        "download_count": download_count,
        "copy_count": copy_count,
        "skipped_count": skipped_count,
        "import_method": method,
        "message": msg
    }

def sync_to_immich(
    url: str, 
    api_key: str, 
    filenames: List[str], 
    is_new_album: bool, 
    album_name: str, 
    tags: List[str], 
    outputs_dir: str
) -> Dict[str, Any]:
    """
    Upload files to Immich with real file timestamps and attach them to Albums and Tags.
    """
    configuration = _get_configuration(url, api_key)
    
    logger.info("--- START IMMICH SYNC (SDK) ---")
    logger.info(f"Params: filenames={len(filenames)}, is_new_album={is_new_album}, album_name={album_name}, tags={tags}")
    
    try:
        with ApiClient(configuration) as api_client:
            asset_api = assets_api.AssetsApi(api_client)
            album_api = albums_api.AlbumsApi(api_client)
            tag_api = tags_api.TagsApi(api_client)
            
            # 1. Resolve Album
            album_id = None
            if album_name:
                albums = album_api.get_all_albums()
                for a in albums:
                    if a.album_name == album_name:
                        album_id = a.id
                        break
                if not album_id:
                    new_album = album_api.create_album(CreateAlbumDto(album_name=album_name))
                    album_id = new_album.id
                logger.info(f"Resolved album_id: {album_id}")
            
            # 2. Resolve Tags
            tag_ids = []
            if tags:
                existing_tags = tag_api.get_all_tags()
                for tag_str in tags:
                    tid = None
                    for t in existing_tags:
                        if t.name.lower() == tag_str.lower():
                            tid = t.id
                            break
                    if not tid:
                        new_tag = tag_api.create_tag(TagCreateDto(name=tag_str))
                        tid = new_tag.id
                    tag_ids.append(tid)
                logger.info(f"Resolved tag_ids: {tag_ids}")
                
            # 3. Upload Assets with real file timestamps
            uploaded_asset_ids = []
            missing_files = []
            duplicate_files = []
            errors = []
            
            for filename in filenames:
                file_path = os.path.join(outputs_dir, filename)
                if not os.path.exists(file_path):
                    missing_files.append(file_path)
                    logger.warning(f"File missing: {file_path}")
                    continue
                    
                # Extract actual creation and modification timestamps
                try:
                    mtime = os.path.getmtime(file_path)
                    file_mtime_utc = datetime.fromtimestamp(mtime, tz=timezone.utc)
                except Exception:
                    file_mtime_utc = datetime.now(timezone.utc)

                try:
                    ctime = os.path.getctime(file_path)
                    file_ctime_utc = datetime.fromtimestamp(ctime, tz=timezone.utc)
                except Exception:
                    file_ctime_utc = file_mtime_utc
                    
                try:
                    logger.debug(f"Uploading file: {filename} (mtime: {file_mtime_utc})")
                    res = asset_api.upload_asset(
                        asset_data=file_path,
                        file_created_at=file_ctime_utc,
                        file_modified_at=file_mtime_utc,
                        filename=filename
                    )
                    
                    uploaded_asset_ids.append(res.id)
                    if hasattr(res, "duplicate") and getattr(res, "duplicate"):
                        duplicate_files.append(filename)
                        
                    logger.debug(f"Upload Response: id={res.id}")
                except Exception as fe:
                    logger.error(f"Upload Exception for {filename}: {fe}")
                    errors.append(f"{filename}: {str(fe)}")

            if not uploaded_asset_ids:
                logger.warning(f"No assets uploaded. Missing: {len(missing_files)}, Errors: {len(errors)}")
                return {
                    "success": False, 
                    "message": f"No assets uploaded. Missing: {len(missing_files)}, Duplicates: {len(duplicate_files)}, Errors: {len(errors)}"
                }
                
            # 4. Attach to Album
            if album_id:
                try:
                    album_api.add_assets_to_album(id=album_id, bulk_ids_dto=BulkIdsDto(ids=uploaded_asset_ids))
                    logger.info("Album PUT Success")
                except Exception as e:
                    logger.error(f"Album PUT Exception: {e}")
                
            # 5. Attach Tags
            if tag_ids:
                try:
                    tag_api.bulk_tag_assets(tag_bulk_assets_dto=TagBulkAssetsDto(asset_ids=uploaded_asset_ids, tag_ids=tag_ids))
                    logger.info("Tag PUT Success")
                except Exception as e:
                    logger.error(f"Tag PUT Exception: {e}")
                
            logger.info("--- END IMMICH SYNC (SUCCESS) ---")
            return {"success": True, "message": f"Exported {len(uploaded_asset_ids)} assets using SDK."}
        
    except Exception as e:
        logger.error(f"Global Immich Sync Exception: {e}", exc_info=True)
        return {"success": False, "message": str(e)}
