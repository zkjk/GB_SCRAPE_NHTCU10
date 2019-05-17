#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author Zakaria El-Bouchahati
# import scrapy and regex AND LinkExtractor
# This program scrapes through the comapnies in the uk website to run it
# enter this link in the command line: scrapy crawl CYR_FINAL -o "name_of_file".json
# as this scrapes every result with "a" cancel with cntrl + c (ONCE!)

import scrapy
import re
from scrapy.linkextractors import LinkExtractor


class QuotesSpider(scrapy.Spider):

  name = 'CYR_FINAL'
  start_urls = [
      'https://www.companiesintheuk.co.uk/Company/Find?q=a']

  def parse(self, response):
    #This part extract the search result item page and makes parse_details method go through it
    for company_url in response.xpath('//div[@class="search_result_title"]/a/@href').extract():
      yield scrapy.Request(
          url=response.urljoin(company_url),
          callback=self.parse_details,
      )

    #This part scrapes through the next search result page
    next_page_url = response.xpath('//li/a[@class="pageNavNextLabel"]/@href').extract_first()
    if next_page_url:
        yield scrapy.Request(
            url=response.urljoin(next_page_url),
            callback=self.parse,
        )

  def parse_details(self, response):
    # Looping throught the searchResult block and yielding it
    for i in response.css('#content2'):
      yield {
          'company_name': i.css('[itemprop="name"]::text').get(),
          'address': i.css('[itemprop="streetAddress"]::text').extract_first(),
          'location': i.css("[itemprop='addressLocality']::text").extract_first(),
          'postal_code': i.css("[itemprop='postalCode']::text").extract_first(),
      }


##############################################################################################
# test code
    # for i in response.css('div.col-md-6'):
    #    if not i.css('#content2 > strong:nth-child(2) > strong:nth-child(1)'):
    #        continue
    #    yield {
    #        'company_name': i.css('#content2 > strong:nth-child(2) > strong:nth-child(1) > div:nth-child(1)::text').get(),
    #        'address': i.css("#content2 > strong:nth-child(2) > address:nth-child(2) > div:nth-child(1) > span:nth-child(1)::text").extract_first(),
    #        'location': i.css("#content2 > strong:nth-child(2) > address:nth-child(2) > div:nth-child(1) > span:nth-child(3)::text").extract_first(),
    #        'postal_code': i.css("#content2 > strong:nth-child(2) > address:nth-child(2) > div:nth-child(1) > a:nth-child(9) > span:nth-child(1)::text").extract_first(),
    #    }
