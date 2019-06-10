def satstac(rasterPath,rasterName):

    from satstac import Catalog, Collection, Item
    import xarray as xr
    import pandas as pd
    import numpy as np
    from matplotlib import pyplot as plt
    import rasterio
    import rasterio.features
    import rasterio.warp
    from shapely import geometry
    import json
    import cartopy

    class REMAStacItem:

        def __init__(self,rasterPath, rasterName):

            self.rasterPath = rasterPath
            self.id      = rasterName
            self.stac_item   = {"id": rasterName[:-4],
                                "rownum": str(rasterName)[0:2],
                                "colnum": str(rasterName)[3:5],
                                "type": "Feature",
                                "bbox": self.calcBBox(),
                                "geometry": self.calcGeometry(),  
                                "units": 'meters',
                                "resolution": 8
                               }

            self.stac_item['properties']=self.createProperties_meta()
            self.stac_item['links'] = self.create_links()





        def calcBBox(self):

            with rasterio.open(self.rasterPath) as dataset:
                bbox = rasterio.warp.transform_bounds(dataset.crs, 'EPSG:4326',dataset.bounds.left,dataset.bounds.bottom,
                                              dataset.bounds.right,dataset.bounds.top)

            #self.bbox=json.loads(json.dumps(geometry.mapping(bbox)))

            return json.loads(json.dumps(bbox))   


        def calcGeometry(self):

            with rasterio.open(self.rasterPath) as dataset:
                profile = dataset.profile
                    # Read the dataset's valid data mask as a ndarray.
                geom = geometry.box(*rasterio.warp.transform_bounds(dataset.crs, 'EPSG:4326',dataset.bounds.left,dataset.bounds.bottom,
                                              dataset.bounds.right,dataset.bounds.top))

            self.geometry=json.loads(json.dumps(geometry.mapping(geom)))

            return json.loads(json.dumps(geometry.mapping(geom)))


        #def createAssetList(self):
         #   pass


        def createProperties_meta(self):
            meta_prop_dict = {}
            with rasterio.open(self.id) as dataset:
                    meta_prop_dict = dataset.meta
                    crs = meta_prop_dict['crs']
                    crs = 'EPSG:'+str(crs.to_epsg())
                    meta_prop_dict['crs'] = crs
                    profile = dataset.profile
            return meta_prop_dict

        
         #   if imdPath:
          #      o = urlparse(imdPath)
           #     if o.scheme == 's3':
            #        s3 = boto3.resource("s3")
             #       bucket = o.netloc
              #      key = o.path.lstrip('/')
               #     obj = s3.Object(bucket, key)
                #    body = obj.get()['Body'].read()
                 #   root = ET.fromstring(body)

                #else:

                 #   tree = ET.parse(imdPath)
                  #  root = tree.getroot()

                #self.metaDataStruct = iterate_OverXML(root, recursionTagList=['IMD', 'IMAGE'])
            #elif vrtPath:
             #   with rasterio.open(vrtPath) as src:
              #      self.metaDataStruct = process_nitf_tags(src.tags())

           # else:
            #    print("no Data Specified")
            #self.eoDict = self.processMetaData_To_Properties(self.metaDataStruct, self.provider, self.license)
            #return json.loads(json.dumps(meta_prop_dict))

        def write_toJSON(self, filename):
            with open(filename, 'w') as fp:
                json.dump(self.stac_item, fp, indent=2)
                
    myStacItem = REMAStacItem(rasterPath,rasterName)
    filename = myStacItem.stac_item['id']+'.json'
    myStacItem.write_toJSON(filename)