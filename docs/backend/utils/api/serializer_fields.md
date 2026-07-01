# API serializer fields

## `ThumbnailImageField`

- Wraps any Django `ImageField` and enforces valid file name/size, optional max length, and optional upload URL generation.
- In `to_representation`, returns either absolute `image`/`thumbnail` URLs (when `use_url=True`) or file names.
- Used to expose `images` on user serializers and anywhere else compact image metadata is needed.

## `NestedChoiceField`

- Supports choice fields where both `value` and `label` are returned.
- Accepts strings, ints, or dicts (with a `value` key) during input, and always serializes into `{ "value": ..., "label": ... }`.
- `allow_blank` enables empty values for optional choices.
