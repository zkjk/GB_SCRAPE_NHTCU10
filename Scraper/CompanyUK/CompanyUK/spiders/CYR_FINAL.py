#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author Zakaria El-Bouchahati

# This program scrapes through the comapnies in the uk website to run it
# enter this link in the command line: scrapy crawl CYR_FINAL -a ip='name_of_search' -o "name_of_file".json
# as this scrapes every result with the saerch query you asked for, cancel with cntrl + c (ONCE!)

# import scrapy and regex AND LinkExtractor AND uuid
import scrapy
from scrapy.linkextractors import LinkExtractor
import datetime
import uuid


class QuotesSpider(scrapy.Spider):

  name = 'CYR_FINAL'
  start_urls = ['https://www.companiesintheuk.co.uk/Company/Find?q=']

  def start_requests(self):
        # self points to the spider instance
        # that was initialized by the scrapy framework when starting a crawl
        # spider instances are "augmented" with crawl arguments
        # available as instance attributes,
        # self.ip has the (string) value passed on the command line
        # with `-a ip=somevalue`
    for url in self.start_urls:
      yield scrapy.Request(url + self.ip, dont_filter=True)

  def parse(self, response):
    # This part extract the search result item page and makes parse_details method go through it
    for company_url in response.xpath('//div[@class="search_result_title"]/a/@href').extract():
      yield scrapy.Request(
          url=response.urljoin(company_url),
          callback=self.parse_details,
      )

    # Extract subsections from the current section
    for section in response.xpath('//a[@id="sic-section-description"]/@href').extract():
      yield scrapy.Request(url=response.urljoin(section), callback=self.parse)

    # This part scrapes through the next search result page
    next_page_url = response.xpath(
        '//li/a[@class="pageNavNextLabel"]/@href').extract_first()
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
          'company_registration_no': i.css('#content2 > div:nth-child(6) > div:nth-child(2)::text').extract_first(),
          'address': i.css('[itemprop="streetAddress"]::text').extract_first(),
          'location': i.css("[itemprop='addressLocality']::text").extract_first(),
          'postal_code': i.css("[itemprop='postalCode']::text").extract_first(),
          'land_code': i.css("test").extract_first(default="GB"),
          'date_time': datetime.datetime.now(),
          'uid': str(uuid.uuid4())
      }
