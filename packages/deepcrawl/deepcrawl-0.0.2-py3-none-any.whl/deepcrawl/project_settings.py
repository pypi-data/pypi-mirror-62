from requests.auth import HTTPBasicAuth
import json

from .api_endpoints import *
from .api_requests import *

# List of project settings fields
project_settings_fields = [
						'alert_emails',
						'alert_setting', 
						'api_callback', 
						'api_callback_headers', 
						'attach_pdf', 
						'auto_finalize', 
						'clean_custom_extraction',
						'custom_extractions',
						'compare_to', 
						'crawl_amphtml_ext', 
						'crawl_amphtml_int', 
						'crawl_canonicals_ext', 
						'crawl_canonicals_int', 
						'crawl_hyperlinks_ext', 
						'crawl_hyperlinks_int', 
						'crawl_hreflangs_ext', 
						'crawl_hreflangs_int', 
						'crawl_images_ext', 
						'crawl_images_int', 
						'crawl_media_mobile_ext', 
						'crawl_media_mobile_int', 
						'crawl_paginations_ext', 
						'crawl_paginations_int', 
						'crawl_redirects_ext', 
						'crawl_redirects_int', 
						'crawl_scripts_ext', 
						'crawl_scripts_int', 
						'crawl_stylesheets_ext', 
						'crawl_stylesheets_int', 
						'crawl_disallow_1st_level', 
						'crawl_not_included_1st_level', 
						'crawl_nofollow', 
						'crawl_noindex', 
						'crawl_non_html', 
						'crawl_css_js', 
						'crawl_disallowed_pages', 
						'crawl_external_urls', 
						'crawl_nofollow_links', 
						'crawl_noindex_pages', 
						'crawl_non_html_file_types', 
						'crawl_not_included_urls', 
						'crawl_rate', 
						'crawl_rate_advanced', 
						'crawl_subdomains', 
						'crawl_http_and_https', 
						'crawl_test_site', 
						'crawl_types', 
						'custom_dns', 
						'custom_header_user_agent', 
						'custom_header_user_agent_short', 
						'is_stealth_mode', 
						'deepcrawl_bot_url', 
						'duplicate_precision', 
						'low_log_summary_requests', 
						'high_log_summary_requests', 
						'limit_levels_max', 
						'limit_pages_max', 
						'location', 
						'max_content_size', 
						'max_description_length', 
						'max_external_links', 
						'max_html_size', 
						'max_links', 
						'max_load_time', 
						'max_redirections', 
						'max_title_width', 
						'max_url_length', 
						'min_content_ratio', 
						'thin_page_threshold', 
						'min_description_length', 
						'min_title_length', 
						'empty_page_threshold', 
						'name', 
						'page_groupings', 
						'robots_overwrite', 
						'site_primary', 
						'site_secondaries', 
						'site_test', 
						'site_test_pass', 
						'site_test_user', 
						'start_urls', 
						'url_rewrite_query_parameters', 
						'url_rewrite_regex_parameters', 
						'url_rewrite_strip_fragment', 
						'urls_excluded', 
						'urls_included', 
						'use_rewrite_rules', 
						'use_robots_overwrite', 
						'user_agent', 
						'mobile_user_agent', 
						'use_robots_for_sitemaps', 
						'active',
						'disable_ssl_verification', 
						'splunk_enabled', 
						'use_mobile_settings', 
						'mobile_url_pattern', 
						'mobile_homepage_url', 
						'mobile_custom_header_user_agent', 
						'mobile_custom_header_user_agent_short', 
						'logzio_enabled', 
						'use_renderer', 
						'renderer_block_ads', 
						'renderer_block_analytics', 
						'renderer_block_custom', 
						'renderer_js_string', 
						'renderer_js_urls', 
						'use_optimus', 
						'is_meridian']

class ProjectSettings:

	# Use slots to save memory and prevent invalid values
	__slots__ = project_settings_fields

	def __init__(self, project_settings={}):
		
		# create attributes for every valid name
		for key, value in project_settings.items():
			if key in project_settings_fields:
				setattr(self, key, value)

	# Create a dictable version of attributes to allow use of slots and vars()
	@property
	def __dict__(self):
		return {s: getattr(self, s) for s in self.__slots__ if hasattr(self, s)}

