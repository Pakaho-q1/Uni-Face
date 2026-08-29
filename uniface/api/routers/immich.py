import os
import uuid
import shutil
import asyncio
import urllib.request
from typing import List, Optional
from fastapi import APIRouter, Header, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io

from uniface.core.workspace import ensure_workspace
from uniface.core.immich_sync import (
    sync_to_immich, 
    test_immich_connection as sdk_test_connection,
    get_immich_albums_list as sdk_get_albums,
    get_immich_tags_list as sdk_get_tags,
    get_immich_people_list as sdk_get_people,
    get_immich_category_assets as sdk_get_category_assets,
    import_immich_assets as sdk_import_assets,
    _normalize_base_url
)
from uniface.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["immich"])

class ImmichTestRequest(BaseModel):
    url: str
    api_key: str

class ImmichExportRequest(BaseModel):
    url: str
    api_key: str
    new_album: bool
    album: str
    tags: List[str]
    filenames: List[str]

class ImmichImportRequest(BaseModel):
    url: str
    api_key: str
    asset_ids: List[str]
    local_path: Optional[str] = None

@router.post("/api/v1/immich/test")
async def test_immich_connection(req: ImmichTestRequest):
    return await asyncio.to_thread(sdk_test_connection, req.url, req.api_key)

@router.get("/api/v1/immich/albums")
async def get_immich_albums(url: str, api_key: str):
    return await asyncio.to_thread(sdk_get_albums, url, api_key)

@router.get("/api/v1/immich/tags")
async def get_immich_tags(url: str, api_key: str):
    return await asyncio.to_thread(sdk_get_tags, url, api_key)

@router.get("/api/v1/immich/people")
async def get_immich_people(url: str, api_key: str):
    return await asyncio.to_thread(sdk_get_people, url, api_key)

@router.get("/api/v1/immich/assets")
async def get_immich_assets(
    url: str, 
    api_key: str, 
    category_type: str = Query(..., pattern="^(people|albums|tags)$"), 
    category_id: str = Query(...)
):
    return await asyncio.to_thread(sdk_get_category_assets, url, api_key, category_type, category_id)

@router.post("/api/v1/immich/import")
async def import_immich_targets(
    req: ImmichImportRequest, 
    x_client_platform: str = Header("unknown")
):
    uploads_dir, _ = ensure_workspace(x_client_platform)
    immich_target_dir = os.path.join(uploads_dir, "immich")
    return await asyncio.to_thread(
        sdk_import_assets, 
        req.url, 
        req.api_key, 
        req.asset_ids, 
        immich_target_dir, 
        req.local_path
    )

@router.get("/api/v1/immich/thumbnail/person/{person_id}")
async def get_person_thumbnail(
    person_id: str, 
    url: str = Query(...), 
    api_key: str = Query(...)
):
    try:
        base_url = _normalize_base_url(url)
        thumb_url = f"{base_url}/api/people/{person_id}/thumbnail"
        req = urllib.request.Request(thumb_url, headers={"x-api-key": api_key})
        
        def fetch_bytes():
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                return resp.read()
                
        content = await asyncio.to_thread(fetch_bytes)
        return Response(content=content, media_type="image/jpeg")
    except Exception as e:
        logger.debug(f"Failed to fetch person thumbnail ({person_id}): {e}")
        raise HTTPException(status_code=404, detail="Thumbnail not found")

@router.get("/api/v1/immich/thumbnail/asset/{asset_id}")
async def get_asset_thumbnail(
    asset_id: str, 
    url: str = Query(...), 
    api_key: str = Query(...)
):
    try:
        base_url = _normalize_base_url(url)
        thumb_url = f"{base_url}/api/assets/{asset_id}/thumbnail"
        req = urllib.request.Request(thumb_url, headers={"x-api-key": api_key})
        
        def fetch_bytes():
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                return resp.read()
                
        content = await asyncio.to_thread(fetch_bytes)
        return Response(content=content, media_type="image/jpeg")
    except Exception as e:
        logger.debug(f"Failed to fetch asset thumbnail ({asset_id}): {e}")
        raise HTTPException(status_code=404, detail="Thumbnail not found")

@router.post("/api/v1/immich/export")
async def export_to_immich(req: ImmichExportRequest, x_client_platform: str = Header("unknown")):
    _, outputs_dir = ensure_workspace(x_client_platform)
    
    temp_dir_name = f"immich_staging_{uuid.uuid4().hex[:8]}"
    temp_dir = os.path.join(outputs_dir, temp_dir_name)
    os.makedirs(temp_dir, exist_ok=True)
    
    staged_filenames = []
    for fn in req.filenames:
        src = os.path.join(outputs_dir, fn)
        dst = os.path.join(temp_dir, fn)
        if os.path.exists(src):
            try:
                try:
                    os.link(src, dst)
                except OSError:
                    shutil.copy2(src, dst)
                staged_filenames.append(fn)
            except Exception as e:
                logger.warning(f"Failed to stage {fn}: {e}")
                
    try:
        result = await asyncio.to_thread(
            sync_to_immich,
            req.url,
            req.api_key,
            staged_filenames,
            req.new_album,
            req.album,
            req.tags,
            temp_dir
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
        
    return result
