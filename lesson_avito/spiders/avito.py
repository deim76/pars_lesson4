# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

from lesson_avito.items import LessonAvitoItem


class AvitoSpider(scrapy.Spider):
    name = 'notes'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/kazan/kvartiry/prodam']

    def parse(self, response: HtmlResponse):
        text_next_page = response.xpath(
            '//span[contains(@data-marker,"pagination-button/next")]/@class').extract_first()
        current_page = int(response.xpath('//span[contains(@class,"pagination-item_active")]/text()').extract_first())
        notes = response.xpath('//a[contains(@class,"snippet-link")]/@href').extract()
        if 'item_arrow' in text_next_page:
            next_page = '/kazan/kvartiry/prodam?p=' + str(current_page + 1)
            yield response.follow(next_page, callback=self.parse)

        for note in notes:
            print(note)
            yield response.follow(note, callback=self.note_parse)

    def note_parse(self, response: HtmlResponse):
        filds = response.xpath(
            '//ul[contains(@class,"item-params-list")]/li[contains(@class,"item-params-list-item")]/span[contains(@class,"item-params-label")]/text()').extract()
        values_response = response.xpath(
            '//ul[contains(@class,"item-params-list")]/li[contains(@class,"item-params-list-item")]/text()').extract()
        values=[]
        for i in values_response:
            if not i==' ':
               values.append(i)


        elements= dict.fromkeys(filds)

        for i in range(0, len(filds)):
            elements[filds[i]] = values[i]

        yield LessonAvitoItem(
            name=response.xpath('//span[contains(@class,"title-info-title-text")]/text()').extract_first(),
            url=response.url,
            price=response.xpath('//span[contains(@class,"js-item-price")]/text()').extract_first(),
            details=elements
        )

