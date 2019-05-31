#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import pandas as pd
import csv


class Insta_Info_Scraper:

    def getinfo(self, url):
        html = urllib.request.urlopen(url, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all('meta', attrs={'property': 'og:description'
                             })
        text = data[0].get('content').split()
        user = '%s %s %s' % (text[-3], text[-2], text[-1])
        followers = int(text[0].replace(',',''))
        following = int(text[2].replace(',',''))
        posts = int(text[4].replace(',',''))
        return user, posts, followers, following

    def main(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        df=pd.read_csv('data/made/verified_accounts_ttvpa_used_to_follow.csv')
        urls=[i for i in df.user_profile]

        for url in urls[:5]:
            user = self.getinfo(url)

            '''record the transaction
            '''  
            # open up the csv
            with open('data/made/test_account_data.csv', 'a') as file:
                # fit the writer
                writer = csv.writer(file)
                # document the transaction
                writer.writerow(user)


if __name__ == '__main__':
    obj = Insta_Info_Scraper()
    obj.main()
