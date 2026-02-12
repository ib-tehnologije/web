# Copyright 2020 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models

from .assetsbundle import AssetsBundleCompanyColor


class QWeb(models.AbstractModel):
    _inherit = "ir.qweb"

    def _generate_asset_links_cache(
        self,
        bundle,
        css=True,
        js=True,
        assets_params=None,
        rtl=False,
    ):
        res = super()._generate_asset_links_cache(
            bundle,
            css=css,
            js=js,
            assets_params=assets_params,
            rtl=rtl,
        )
        if bundle == "web_company_color.company_color_assets":
            asset = AssetsBundleCompanyColor(
                bundle, [], env=self.env, css=True, js=True
            )
            res += [asset.get_company_color_asset_node()]
        return res

    def _generate_asset_links(
        self,
        bundle,
        css=True,
        js=True,
        debug_assets=False,
        assets_params=None,
        rtl=False,
    ):
        res = super()._generate_asset_links(
            bundle,
            css=css,
            js=js,
            debug_assets=debug_assets,
            assets_params=assets_params,
            rtl=rtl,
        )
        if bundle == "web_company_color.company_color_assets":
            asset = AssetsBundleCompanyColor(
                bundle, [], env=self.env, css=True, js=True
            )
            res += [asset.get_company_color_asset_node()]
        return res

    def _get_asset_content(self, bundle, assets_params=None):
        """Handle 'special' web_company_color bundle"""
        if bundle == "web_company_color.company_color_assets":
            return [], []
        return super()._get_asset_content(bundle, assets_params=assets_params)

    def _get_asset_nodes(
        self,
        bundle,
        css=True,
        js=True,
        debug=False,
        defer_load=False,
        lazy_load=False,
        media=None,
    ):
        res = super()._get_asset_nodes(
            bundle,
            css=css,
            js=js,
            debug=debug,
            defer_load=defer_load,
            lazy_load=lazy_load,
            media=media,
        )
        if isinstance(res, list):
            # In some edge cases (eg. asset resolution failures) Odoo may return
            # placeholder entries. Remove them to avoid breaking rendering.
            res = [n for n in res if n is not None]
        # Odoo may return nodes of different shapes (or placeholders) depending
        # on asset resolution. Be defensive to avoid breaking the whole webclient.
        for node in res or []:
            if (
                not node
                or not isinstance(node, (list, tuple))
                or len(node) < 2
                or not isinstance(node[0], str)
                or not isinstance(node[1], dict)
            ):
                continue
            tag, attributes = node[0], node[1]
            if tag == "link" and attributes.get("href", "").startswith(
                "/web_company_color/static/src/scss/custom_colors."
            ):
                attributes.pop("type", None)
        return res
