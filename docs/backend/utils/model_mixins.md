# Mixins defined in `utils/model_mixins.py`

## Summary
- [`ImageMixin`](#imagemixin) — image URL helpers for models that expose `image_url`/`thumb_url`; see the [Reference](#reference) entry for properties and methods.
- [`DownloadSizeMixin`](#downloadsizemixin) — aggregates issue download sizes using `filesizeformat`; details in the [Reference](#reference) entry.
- [`AliasesListMixin`](#aliaseslistmixin) — splits stored alias strings; refer to the [Reference](#reference) entry for method signatures.
- Protocols [`HasIssuesProtocol`](#hasissuesprotocol) and [`HasAliasesProtocol`](#hasaliasesprotocol) describe the attributes expected by the mixins; see the [Reference](#reference) section for details.

## Reference

### `ImageMixin`
- Provides URL helpers for models that store `image_url` and `thumb_url` fields.

#### Attributes & properties
- `image_url`, `thumb_url`: Expected string/URL fields on the consuming model.
- `full_size_url`: Returns `image_url` when present, otherwise `None`.
- `thumb_size_url`: Returns `thumb_url` when present.
- `square_avatar`, `square_tiny`, `square_small`, `square_medium`: Shortcut properties that call `get_image_size` with the corresponding size label.

#### Methods
- `get_image_size(self, size)`
  - `size`: Size token to request (e.g., `square_avatar`).
  - Rewrites the thumbnail URL path to request the requested size variant; returns `None` when no thumbnail URL exists.

### `HasIssuesProtocol`
- Protocol that declares an `.issues` attribute (a Django `QuerySet`) so mixins can aggregate data from related issue records.

### `DownloadSizeMixin`
- Depends on `HasIssuesProtocol` to access `.issues`.

#### Properties
- `download_size`
  - Aggregates the total `size` for issues where `comicvine_status="MATCHED"` and formats the value via `filesizeformat`.
  - Returns a string like "4.5 MB".

### `HasAliasesProtocol`
- Protocol defining an `.aliases` text field (newline-delimited) so alias helpers can consume it safely.

### `AliasesListMixin`
- Depends on `HasAliasesProtocol` to split the stored aliases string.

#### Methods
- `get_aliases_list(self)`
  - Splits `aliases` on newline characters.
  - Returns an empty list when `aliases` is falsy, otherwise returns the list of trimmed entries.
