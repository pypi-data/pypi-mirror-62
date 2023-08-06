import numpy as np
import os
import gzip

from vtkplotter import Volume, load

# TODO see if this can be added to setup.py
try:
    from mcmodels.core import VoxelModelCache
    from mcmodels.core import Mask
except ModuleNotFoundError:
    raise ModuleNotFoundError("To use this functionality you need to install mcmodels "+
                            "with: 'pip install git+https://github.com/AllenInstitute/mouse_connectivity_models.git'")

from brainrender.Utils.paths_manager import Paths
from brainrender.scene import Scene
from brainrender.Utils.data_io import connected_to_internet


class VolumetricAPI(Paths):
    """
        This class takes care of downloading, analysing and rendering data from:
        "High-resolution data-driven model of the mouse connectome ", Knox et al 2018.
        [https://www.mitpressjournals.org/doi/full/10.1162/netn_a_00066].

        These data can be used to look at spatialised projection strength with sub-region (100um) resolution.
        e.g. to look at where in region B are the projections from region A, you can use this class.

        To download the data, this class uses code from: https://github.com/AllenInstitute/mouse_connectivity_models.
    """
    voxel_size = 100

    projections = {}
    mapped_projections = {}

    hemispheres = dict(left=1, right=2, both=3)

    def __init__(self, base_dir=None, add_root=True, scene_kwargs={}, **kwargs):
        """
            Initialise the class instance to get a few useful paths and variables. 

            :param base_dir: str, path to base directory in which all of brainrender data are stored. 
                    Pass only if you want to use a different one from what's default.
            :param add_root: bool, if True the root mesh is added to the rendered scene
            :param scene_kwargs: dict, params passed to the instance of Scene associated with this class
        """
        Paths.__init__(self, base_dir=base_dir, **kwargs)

        # Get MCM cache
        cache_path = os.path.join(self.mouse_connectivity_volumetric, 'voxel_model_manifest.json')

        if not os.path.isfile(cache_path):
            if not connected_to_internet():
                raise ValueError("The first time you use this class it will need to download some data, but it seems that you're not connected to the internet.")
            print("Downloading volumetric data. This will take several minutes but it only needs to be done once.")

        self.cache = VoxelModelCache(manifest_file=cache_path)
        self.voxel_array = None

        # Get projection cache paths
        self.data_cache = self.mouse_connectivity_volumetric_cache
        self.data_cache_projections = os.path.join(self.data_cache, "projections")
        self.data_cache_targets = os.path.join(self.data_cache, "targets")
        self.data_cache_sources = os.path.join(self.data_cache, "sources")

        for fold in [self.data_cache_projections, self.data_cache_targets, 
                            self.data_cache_sources]:
            if not os.path.isdir(fold):
                os.mkdir(fold)

        # Get structures tree
        self.structure_tree = self.cache.get_structure_tree()

        # Get scene
        self.scene = Scene(add_root=add_root, **scene_kwargs)

    def _get_structure_id(self, struct):
        " Get the ID of a structure (or list of structures) given it's acronym"
        if not isinstance(struct, (list, tuple)): 
            struct = [struct]
        return [self.structure_tree.get_structures_by_acronym([s])[0]["id"] for s in struct]

    def _load_voxel_data(self):
        "Load the VoxelData array from Knox et al 2018"
        if self.voxel_array is None:
            print("Loading voxel data, might take a few minutes.")
            self.voxel_array, self.source_mask, self.target_mask = self.cache.get_voxel_connectivity_array()

    def _get_cache_filename(self, tgt, what):
        """Data are cached according to a naming convention, this function gets the name for an object
        according to the convention"""
        if what == 'projection':
            fld = self.data_cache_projections
        elif what == 'source':
            fld = self.data_cache_sources
        elif what == 'target':
            fld = self.data_cache_targets
        else:
            raise ValueError(f'Error while getting cached data file name.\n'+
                            f'What was {what} but should be projection/source/target/actor.')

        name = ''.join([str(i) for i in tgt])
        path = os.path.join(fld, name+'.npy.gz')
        return name, path, os.path.isfile(path)

    def _get_from_cache(self, tgt, what):
        """ tries to load objects from cached data, if they exist"""
        name, cache_path, cache_exists = self._get_cache_filename(tgt, what)
        if not cache_exists:
            return None
        else:
            f = gzip.GzipFile(cache_path, "r")
            return np.load(f)

    def save_to_cache(self, tgt, what, obj):
        """ Saves data to cache to avoid loading thema again in the future"""
        name, cache_path, _ = self._get_cache_filename(tgt, what)

        f = gzip.GzipFile(cache_path, "w")
        np.save(f, obj)

    def get_source(self, source, hemisphere='both'):
        """
            Loads the mask for a source structure

            :param source: str or list of str with acronym of source regions
            :param hemisphere: str, ['both', 'left', 'right']. Which hemisphere to consider.
        """
        if not isinstance(source, (list, tuple)): 
            source = [source]

        self.source = self._get_from_cache(source, 'source')
        if self.source is None:
            self._load_voxel_data()
            source_ids = self._get_structure_id(source)

            self.source = self.source_mask.get_structure_indices(structure_ids=source_ids, 
                                    hemisphere_id=self.hemispheres[hemisphere])
            self.save_to_cache(source, 'source', self.source)
        return self.source

    def get_target_mask(self, target, hemisphere):
        """returns a 'key' array and a mask object
            used to transform projection data from linear arrays to 3D volumes.
        """
        target_ids = self._get_structure_id(target)
        self.tgt_mask = Mask.from_cache(self.cache, structure_ids=target_ids, 
                        hemisphere_id=self.hemispheres[hemisphere])
        self.tgt_key = self.tgt_mask.get_key()

    def get_target(self, target, hemisphere='both'):
        """
            Loads the mask for a target structure.  

            :param target: str or list of str with acronym of target regions
            :param hemisphere: str, ['both', 'left', 'right']. Which hemisphere to consider.
        """
        if not isinstance(target, (list, tuple)): 
            target = [target]

        if hemisphere != 'both':
            cache_name = target + [hemisphere]
        else:
            cache_name = target

        self.target = self._get_from_cache(cache_name, 'target')
        if self.target is None:
            self._load_voxel_data()
            target_ids = self._get_structure_id(target)

            self.target = self.target_mask.get_structure_indices(structure_ids=target_ids, 
                                    hemisphere_id=self.hemispheres[hemisphere])
            self.save_to_cache(cache_name, 'target', self.target)

        return self.target

    def get_projection(self, source, target, name,  hemisphere='both',
                             projection_mode='mean', mode='target'):
        """
                Gets the spatialised projection intensity from a source to a target. 

                :param source: str or list of str with acronym of source regions
                :param target: str or list of str with acronym of target regions
                :param name: str, name of the projection
                :param projection_mode: str, if 'mean' the data from different experiments are averaged, 
                                    if 'max' the highest value is taken.
                :param mode: str. If 'target' the spatialised projection strength in the target structures is returned, usefule
                        to see where source projects to in target. Otherwise if 'source' the spatialised projection strength in
                        the source structure is return. Useful to see which part of source projects to target.

                :return: 1D numpy array with mean projection from source to target voxels
        """
        if mode == 'target':
            self.get_target_mask(target, hemisphere)
        elif mode == 'source':
            self.get_target_mask(source, 'right')
        else:
            raise ValueError(f'Invalide mode: {mode}. Should be either source or target.')

        cache_name = sorted(source)+['_']+sorted(target)+[f'_{projection_mode}_{mode}']
        if hemisphere != 'both':
            cache_name += [hemisphere]

        proj = self._get_from_cache(cache_name, 'projection')
        if proj is None:
            source_idx = self.get_source(source, hemisphere)
            target_idx = self.get_target(target, hemisphere)

            self._load_voxel_data()
            projection = self.voxel_array[source_idx, target_idx]
            
            if mode == 'target':
                axis = 0
            elif mode == 'source':
                axis = 1
            else:
                raise ValueError(f'Invalide mode: {mode}. Should be either source or target.')

            if projection_mode == 'mean':
                proj = np.mean(projection, axis=axis)
            elif projection_mode == 'max':
                proj = np.max(projection, axis=axis)
            else:
                raise ValueError(f'Projection mode {projection_mode} not recognized.\n'+
                                'Should be one of: ["mean", "max"].')
            
            # Save to cache
            self.save_to_cache(cache_name, 'projection', proj)
        self.projections[name] = proj
        return proj

    def get_mapped_projection(self, source, target, name, **kwargs):
        """
            Gets the spatialised projection intensity from a source to a target, but as 
            a mapped volume instead of a linear array. 

            :param source: str or list of str with acronym of source regions
            :param target: str or list of str with acronym of target regions
            :param name: str, name of the projection

            :return: 3D numpy array with projectino intensity
        """
        projection = self.get_projection(source, target, name, **kwargs)
        mapped_projection = self.tgt_mask.map_masked_to_annotation(projection)
        self.mapped_projections[name] = mapped_projection
        return mapped_projection

    def render_mapped_projection(self, source, target, 
                        std_above_mean_threshold=5,
                        cmap='Greens', alpha=.5,
                        render_source_region=False,
                        render_target_region=False,
                        regions_kwargs={},
                        add_colorbar = True,
                        **kwargs):
        """
            Gets the spatialised projection intensity from a source to a target
            and renders it as a vtkplotter lego visualisation.

            :param source: str or list of str with acronym of source regions
            :param target: str or list of str with acronym of target regions
            :param cmap: str with name of colormap to use
            :param alpha: float, transparency
            :param std_above_mean_threshold: the vmin used to threshold the data is the mean 
                    of the projection strength + this number of standard deviations. Higher values
                    means that more data are excluded from the visualization.
            :param render_source_region: bool, if true a wireframe mesh of source regions is rendered
            :param render_target_region: bool, if true a wireframe mesh of target regions is rendered
            :param regions_kwargs: pass options to specify how brain regions should look like
            :param add_colorbar: if True a colorbar is added to show the values of the colormap
        """
        # Parse kwargs
        vmin = kwargs.pop('vmin', None)
        vmax = kwargs.pop('vmax', None)
        line_width = kwargs.pop('line_width', 1)

        # Get projection data
        if not isinstance(source, list): source = [source]
        if not isinstance(target, list): target = [target]
        name = ''.join(source)+'_'.join(target)
        mapped_projection = self.get_mapped_projection(source, target, name, **kwargs)

        # Get vmin and vmax threshold for visualisation
        if vmin is None:
            vmin = np.mean(mapped_projection)
        vmin += std_above_mean_threshold*np.std(mapped_projection)

        if vmax is None:
            vmax = np.max(mapped_projection)
        else:
            if np.max(mapped_projection) > vmax:
                print("While rendering mapped projection some of the values are above the vmax threshold."+
                            "They will not be displayed."+
                            f" vmax was {vmax} but found value {round(np.max(mapped_projection), 5)}.")

        # Get 'lego' actor
        vol = Volume(mapped_projection)
        lego = vol.legosurface(vmin=vmin, vmax=vmax, 
                                cmap=cmap)

        # Scale and color actor
        lego.alpha(alpha).lw(line_width).scale(self.voxel_size)
        lego.cmap = cmap

        # Add colorbar
        if add_colorbar:
            lego.addScalarBar(vmin=vmin, vmax=vmax, horizontal=1, c='k', 
                            pos=(0.05,0.05), titleFontSize=40)

        # Add to scene
        actor = self.scene.add_vtkactor(lego)

        # Render relevant regions meshes
        if render_source_region or render_target_region:
            wireframe = regions_kwargs.pop('wireframe', True)
            use_original_color = regions_kwargs.pop('use_original_color', True)

            if render_source_region:
                self.scene.add_brain_regions(source, use_original_color=use_original_color, 
                            wireframe=wireframe, **regions_kwargs)
            if render_target_region:
                self.scene.add_brain_regions(target, use_original_color=use_original_color, 
                            wireframe=wireframe, **regions_kwargs)
        return actor
    
    def render(self, **kwargs):
        """
            Renders the scene associated with the class
        """
        self.scene.render(**kwargs)

