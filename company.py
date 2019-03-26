#!/usr/bin/python
# -*- coding: utf-8 -*-
# author Zakaria El-Bouchahati

import scrapy


class QuotesSpider(scrapy.Spider):

  name = 'company'
  start_urls = [
      'https://www.companiesintheuk.co.uk/Company/Find?q=a&location=&s=s']

  def parse(self, response):

    # Looping throught the searchResult block and yielding the company name and address
    for i in response.css('div.searchResult'):
      yield {
          'company_name': i.css('div.search_result_title a::text').get(),
          'address': i.css('div.searchAddress::text').get(),
      }

    # Here I go through all the pages, I do this by selecting the css selector for the next page
    next_page_url = response.css(
        'a.pageNavNextLabel::attr(href)').extract_first()
    # As long as tehre is a next page we go over the main mathod.
    if next_page_url:
      next_page_url = response.urljoin(next_page_url)
      yield scrapy.Request(url=next_page_url, callback=self.parse)
