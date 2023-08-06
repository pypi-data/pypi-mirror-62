"""
    This tutorial shows how to use the VolumetricAPI to download and render spatialised projection strength.
    This can be used to show where inputs from brain region A localise within brain region B

"""

import brainrender
brainrender.SHADER_STYLE = 'cartoon'


from brainrender.Utils.ABA.volumetric.VolumetricConnectomeAPI import VolumetricAPI




vapi = VolumetricAPI(add_root=False, title='Motor cortex projections to ZI')

# Get projections from the primary and secondary motor cortices to the zona incerta
source = ['MOs', 'MOp']
target = 'ZI'
vapi.render_mapped_projection(
            source, 
            target,
            cmap='gist_heat', # specify which heatmap to show
            alpha=1,
            render_target_region=True, # render the targer region
            regions_kwargs={
                        'wireframe':False, 
                        'alpha':.3, 
                        'use_original_color':False},
            mode='target',
            )

vapi.render(zoom=1.1)  

    

