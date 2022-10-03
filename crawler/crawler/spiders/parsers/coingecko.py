import json
import re
from typing import Union
from .base import BaseParser


class CoinGeckoParser(BaseParser):

    def __init__(self, response):
        self.response = response

    @property
    def get_from_json(self):
        xpath = '//script[@type="application/ld+json"][2]/text()'
        return json.loads(self.response.xpath(xpath).get())

    @property
    def get_info(self):
        xpath = '//div[@data-target="coins-information.mobileOptionalInfo"]/div[contains(@class, "coin-link-row")]'
        return self.response.xpath(xpath)

    # FIELDS
    @property
    def name(self) -> str:
        xpath = '//div[contains(text(), "Rank #")]/following-sibling::div/div'
        _v = re.findall(r'\((.*)\)', self.response.xpath(xpath).get())[0]
        return re.sub(r'\((.*)\)', '', _v).strip()

    # FIELDS
    @property
    def symbol(self) -> str:
        xpath = '//div[contains(text(), "Rank #")]/following-sibling::div/div'
        _v = re.findall(r'\((.*)\)', self.response.xpath(xpath).get())[0]
        return _v

    # FIELDS
    @property
    def slug(self) -> str:
        xpath = '//a/@data-source'
        slug = self.response.xpath(xpath).get()
        return slug

    # FIELDS
    @property
    def rank(self) -> Union[int, None]:
        xpath = '//div[contains(text(), "Rank #")]/text()'
        _v = re.sub(r'\D+', '', self.response.xpath(xpath).get())
        return int(_v) if _v else None

    # FIELDS
    @property
    def tags(self) -> Union[list, None]:
        xpath = 'descendant::*[contains(text(), "Tags")]/following-sibling::div//a/text()'
        _t = self.get_info.xpath(xpath).getall()
        _v = [i.lower().replace(' ', '-') for i in self.get_info.xpath(xpath).getall()]
        return _v if _v else None

    # FIELDS
    @property
    def cm_id(self) -> str:
        xpath = '//input[@name="coin_id"]/@value'
        return str(self.response.xpath(xpath).get())

    # FIELDS
    @property
    def logo_url(self) -> Union[str, None]:
        xpath = '//meta[@name="twitter:image"]/@content'
        _v = self.response.xpath(xpath).get()
        return _v if _v else None

    # FIELDS
    @property
    def date_added(self) -> None:
        return

    # FIELDS_META
    @property
    def website(self) -> Union[list, None]:
        xpath = 'descendant::*[contains(text(), "Website")]/following-sibling::div/a/@href'
        _v = self.get_info.xpath(xpath).getall()
        return _v if _v else None

    # FIELDS_META
    @property
    def source_code(self) -> Union[list, None]:
        xpath = 'descendant::*[contains(text(), "Source Code")]/following-sibling::div/a/@href'
        _v = self.get_info.xpath(xpath).getall()
        return _v if _v else None

    # FIELDS_META
    @property
    def explorers(self) -> Union[list, None]:
        xpath = 'descendant::*[contains(text(), "Explorers")]/following-sibling::div//@href'
        _v = self.get_info.xpath(xpath).getall()
        return _v if _v else None

    # FIELDS_META
    @property
    def community(self) -> Union[list, None]:
        xpath = 'descendant::*[contains(text(), "Community")]/following-sibling::div/a/@href'
        _v = self.get_info.xpath(xpath).getall()
        return _v if _v else None

    # FIELDS_META
    @property
    def search_on(self) -> Union[list, None]:
        xpath = 'descendant::*[contains(text(), "Search on")]/following-sibling::a//@href'
        _v = self.get_info.xpath(xpath).getall()
        return _v if _v else None

    # FIELDS_META
    @property
    def wallets(self) -> Union[list, None]:
        xpath = 'descendant::*[contains(text(), "Wallets")]/following-sibling::div/a/@href'
        _v = self.get_info.xpath(xpath).getall()
        return _v if _v else None

    # FIELDS_META
    @property
    def stars(self) -> Union[int, None]:
        xpath = '//i[contains(@class, "star-color")]/parent::*//text()'
        _v = self.get_info.xpath(xpath).getall()
        return int(re.sub(r"\D+", '', ''.join(set(_v)))) if _v else None

    # FIELDS_META
    @property
    def technical_doc(self) -> None:
        return

    # FIELDS_META
    @property
    def audit_infos(self) -> None:
        return
