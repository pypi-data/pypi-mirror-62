# BindFigma

BindFigma is a preprocessor that downloads and optionally resizes design layout images from [Figma](https://www.figma.com/), and binds these images with the documentation project.

The preprocessor uses [Figma REST API](https://www.figma.com/developers/api) to get URLs of images to download. To use the preprocessor, you should get an [access token](https://www.figma.com/developers/api#access-tokens) for it via your Figma account.

If you need to resize downloaded images, you should install [ImageMagick](https://imagemagick.org/).

## Installation

```bash
$ pip install foliantcontrib.bindfigma
```

## Config

To enable the preprocessor, add `bindfigma` to `preprocessors` section in the project config:

```yaml
preprocessors:
    - bindfigma
```

The preprocessor has a number of options with the following default values:

```yaml
preprocessors:
    - bindfigma:
        cache_dir: !path .bindfigmacache
        convert_path: convert
        caption: ''
        hyperlinks: true
        multi_delimeter: '\n\n'
        resize: null
        access_token: null
        file_key: null
        ids: null
        scale: null
        format: null
        svg_include_id: null
        svg_simplify_stroke: null
        use_absolute_bounds: null
        version: null
```

Some values of options specified in the project config may be overridden by tag attributes, see below.

`cache_dir`
:   Directory to store downloaded and resized images.

`convert_path`
:   Path to `convert` binary, a part of ImageMagick. If resizing is not needed, ImageMagick will not be used.

`caption`
:   Caption of images. The `{{image_id}}` placeholder in the caption will be replaced with Figma node ID.

`hyperlinks`
:   Flag that tells the preprocessor to wrap image references into hyperlinks to related Figma URLs.

`multi_delimeter`
:   String that should separate multiple image references.

`resize`
:   Width of resulting images in pixels. If not specified, resizing is not performed.

`access_token`
:   Access token that you can generate in your Figma account.

`file_key`
:   ID of the Figma file.

`ids`
:   One or more IDs of nodes in the Figma file. May be specified as a list or as a comma-separated string.

`scale`, `format`, `svg_include_id`, `svg_simplify_stroke`, `use_absolute_bounds`, `version`
:   Query parameters to use in Figma API requests, see descriptions in [Figma API documentation](https://www.figma.com/developers/api#get-images-endpoint).

## Usage

To insert a design layout image from Figma into your documentation, use `<<figma>...</figma>` tags in Markdown source:

```markdown
Here’s an image from Figma:

<<figma caption="An optional caption" resize="300" file_key="ABC" ids="node1,node2,node3"></figma>
```

You may use tag attributes to override the values of the project config options with the same names. All the options excepting `cache_dir` and `convert_path` may be overridden in this way.

BindFigma preprocessor will replace such statements with local image references. If `ids` refers to more than one image, a set of image references will be generated. Multiple image references will be separated with the string specified as `multi_delimeter`.
