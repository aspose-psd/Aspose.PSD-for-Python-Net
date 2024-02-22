# Aspose.PSD-for-Python-Net
Aspose.PSD for Python examples, plugins and showcases 

## PSD, PSB, AI Manipulation API

**[Aspose.PSD for Python via .NET](https://products.aspose.com/psd/python-net)** is an **Unique Python PSD Library** offering advanced PSD, PSD and AI files processing features. You could easily create, load, update, edit, convert, compress PSD and PSB images using this API. Aspose.PSD Supports most popular features for PSD and PSB files including updates of Text Layers, Smart Objects, Fill Layers, Shape Layers, Group Layers, Adjustment Layers. **Aspose.PSD** supports Blendings Modes, Layer Effects, Warp Transformations, Smart Filters, Animation TimeLine, Working with Vector, Raster and Clipping Masks, Low-Level PSD file resource exploring and much more. Also, library supports drawing and work with graphic primitives for Regular Layers. **Aspose.PSD** is able to export and convert PSD, PSB, AI formats to PNG, TIFF, PDF, JPEG, GIF, BMP. IT supports popular combinations of Bit Depths and Color Modes. Besides the all described a many common tranformation like Layer Resize, Crop, Shift, Rotating are supported too. This is an ultimate PSD, PSB and AI Format Processing Library for any use-cases. It's crossplatform: Windows, MacOS, MacOS-ARM, Linux are supported.

<p align="center"> 
  <a title="Download ZIP" href="https://github.com/aspose-psd/Aspose.PSD-for-Python-Net/archive/refs/heads/main.zip">
     <img src="http://i.imgur.com/hwNhrGZ.png" />
  </a>
</p>

Directory | Description
--------- | -----------
[Examples](Examples)  | A collection of Python examples that help you learn the product features.

## Aspose.PSD Features

- [Create PSD and PSB images from scratch](https://docs.aspose.com/psd/python-net/create-psd-psb-images-from-scratch/)
- [Open and Export of PSD, PSB and AI images to PDF, JPEG, PNG, TIFF, BMP, GIF, BMP](https://docs.aspose.com/psd/python-net/open-export-psd-psb-ai-images-to-pdf-jpeg-png-tiff-bmp-gif-bmp/)
- [Aspose.PSD Team actively work on manipulation with AI files](https://docs.aspose.com/psd/python-net/ai-file-manipulation/)
- [Update PSD and PSB images](https://docs.aspose.com/psd/python-net/update-psd-psb-files-with-python/)
- [Adding of JPEG, PNG, TIFF, BMP, GIF, BMP files as a layers for editing](https://docs.aspose.com/psd/python-net/add-layer-from-file-for-editing/)
- Support of layers: [Regular Layer](https://docs.aspose.com/psd/python-net/psd-layer-manipulation/), [Text Layer](https://docs.aspose.com/psd/python-net/psd-text-layer-manipulation/), [Smart Object](https://docs.aspose.com/psd/python-net/psd-smart-object-update/), [Group Layer](https://docs.aspose.com/psd/python-net/psd-group-layer/), [Adjustment Layer](https://docs.aspose.com/psd/python-net/psd-adjustment-layer-enhancement/), [Fill Layer](https://docs.aspose.com/psd/python-net/psd-fill-layer-editing/), [Shape Layer](https://docs.aspose.com/psd/python-net/psd-shape-layer-manipulation/)
- Support of [Blending Options](https://docs.aspose.com/psd/python-net/blending-options/), [Layer Effects](https://docs.aspose.com/psd/python-net/layer-effects/), [Raster, Vector andd Clipping Masks](https://docs.aspose.com/psd/python-net/update-create-layer-mask/), [Warp Transformations](https://docs.aspose.com/psd/python-net/warp-transform/), [Smart Filters](https://docs.aspose.com/psd/python-net/smart-filters/)
- [Draw lines, circles, ellipses, texts, complex paths, and images using the classes Graphics](https://docs.aspose.com/psd/python-net/graphics-api/)
- [Process images (including per-pixel modifications)](https://docs.aspose.com/psd/python-net/pixel-data-manipulation/)
- [Convert PSD and PSB Files  between different Color Modes and Bit Depths](https://docs.aspose.com/psd/python-net/bit-depth-color-mode-convert/)
- And much more. Please check [documentation page](https://docs.aspose.com/psd/python-net/)

<p align="center"> 
     <img src="https://raw.githubusercontent.com/aspose-psd/Aspose.PSD-for-Python-Net/main/showcase-image.png" alt="Showcase for PSD Automation" Title="Showcase Image for PSD Automation"/>
</p>


## Aspose.PSD Supported formats

**Open for manipulation and export:** PSD, PSB, AI
**Ability to add as a layer for manipulation:** PDF, JPEG, JPEG2000, TIFF, PNG, GIF, BMP \
**Formats to which you can export:** PSD, PSB, PDF, JPEG, JPEG2000, TIFF, PNG, GIF, BMP \

## Platform Independence

Aspose.PSD for Python via .NET can be used to develop applications on Windows Desktop (x86, x64), Windows Server (x86, x64), Windows Azure, as well as Linux x64, MacOS and MacOS-ARM. 

## Get Started with Aspose.PSD for Python via .NET

Are you ready to give Aspose.PSD for Python via .NET a try? Simply execute run this command: `pip install aspose-psd`.

### Open PSD File in Python and update text
``` python

from aspose.psd import Image
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import TextLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions
from aspose.pycore import cast

# Specify File Paths
sourceFile = "AllTypesLayerPsd.psd"
outputFile = "LoadImageExample.png"

# Specify Load Options
loadOptions = PsdLoadOptions()
loadOptions.load_effects_resource = True
loadOptions.allow_warp_repaint = True

# Specify Export Options
exportOptions = PngOptions()
exportOptions.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

# Open File using Aspose.PSD for Python
with Image.load(sourceFile, loadOptions) as image:
    # Types of Aspose.PSD can be casted
    psdImage = cast(PsdImage, image)
    textLayer = cast(TextLayer, psdImage.layers[5])
    textLayer.update_text("Simple Text Edit")

    # Export PSD File To PNG
    psdImage.save(outputFile, exportOptions)
	
```

### Create a PSD File From Scratch. Create Regular Layer using Graphics API and Create Text Layer with Shadow Effect
``` python

from aspose.psd import Graphics, Pen, Color, Rectangle
from aspose.psd.brushes import LinearGradientBrush
from aspose.psd.fileformats.psd import PsdImage

outputFile = "CreateFileFromScratchExample.psd"

# Create PSD Image with specified dimensions
with PsdImage(500, 500) as img:
    # Create Regular PSD Layer and update it with Graphic API
    regularLayer = img.add_regular_layer()

    # Use popular Graphic API for Editing
    graphics = Graphics(regularLayer)
    pen = Pen(Color.alice_blue)
    brush = LinearGradientBrush(Rectangle(250, 250, 150, 100), Color.red, Color.aquamarine, 45)
    graphics.draw_ellipse(pen, Rectangle(100, 100, 200, 200))
    graphics.fill_ellipse(brush, Rectangle(250, 250, 150, 100))

    # Create Text Layer
    textLayer = img.add_text_layer("Sample Text", Rectangle(200, 200, 100, 100))

    # Adding Shadow to Text
    dropShadowEffect = textLayer.blending_options.add_drop_shadow()
    dropShadowEffect.distance = 0
    dropShadowEffect.size = 8
    dropShadowEffect.color = Color.blue

    # Save PSD File
    img.save(outputFile)
```

### Add Image File as a Layer or Open Image File as a PSD
``` python

from io import BytesIO
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import Layer

inputFile = "inputFile.png"
outputFile = "AddFileAsLayer.psd"

# Open file as Stream
with open(inputFile, "rb", buffering=0) as filestream:
    stream = BytesIO(filestream.read())
    stream.seek(0)

    # Create PSD Layer from Stream
    layer = Layer(stream)

    # Create PSD Image with the specified size
    psdImage = PsdImage(layer.width, layer.height)

    # Add Layer to PSD Image
    psdImage.layers = [layer]

    # Get Pixels from File
    pixels = layer.load_argb_32_pixels(layer.bounds)
    pixelsRange = range(len(pixels))

    # Fill the pixels data with some values
    for i in pixelsRange:
        if i % 5 == 0:
            pixels[i] = 500000

    # Fast Save of Updated Image Data
    layer.save_argb_32_pixels(layer.bounds, pixels)

    # Save PSD Image
    psdImage.save(outputFile)
```


### Set License Example
``` python

from aspose.psd import License

license = License()
licensePath = "PathToLicenseFile"
license.set_license(licensePath)
    
```

---
[Product Page](https://products.aspose.com/psd/python-net/) | [Documentation](https://docs.aspose.com/psd/python-net/) | [Demos](https://products.aspose.app/psd/family) | [Blog](https://blog.aspose.com/categories/aspose.psd-product-family/) | [API Reference](https://reference.aspose.com/psd/python-net/) | [Search](https://search.aspose.com/) | [Free Support](https://forum.aspose.com/c/psd) | [Temporary License](https://purchase.aspose.com/temporary-license) | [EULA](https://company.aspose.com/legal/eula)

