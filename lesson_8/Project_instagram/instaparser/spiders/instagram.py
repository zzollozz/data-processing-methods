import re
import json
import scrapy
from copy import deepcopy
from urllib.parse import urlencode
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem



class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login_link = "https://www.instagram.com/accounts/login/ajax/"
    inst_login = '********'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1643977371:AR1QANiFCBakfTRUIPbN6NdRRr0WES8nbChDu+c5RJdzpbgUNwZ2xHnrVQbYTT5LblD3e0yedLxKizur+MB1Q0rk/XWh/sZ6xOYOKJhoQxkTaN4Uno1K10KwR1p8OrOWa7Fp1Z3MkHuoue+0dGhvDg=='
    user_for_parses = ['techskills_2022']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'
    subscriptions_link = 'https://i.instagram.com/api/v1/friendships/{}/'
    user_info_link = 'https://i.instagram.com/api/v1/users/{}/info/'

    def parse(self, response: HtmlResponse): # login_account_root
        ''' Проходим Индификацию '''
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.account_root,
            formdata={'username': self.inst_login,
                      'enc_password': self.inst_pwd},
            headers={'X-CSRFToken': csrf}
        )

    def account_root(self, response: HtmlResponse):
        ''' Проходим уже со своего Ака дальше куда нужно '''
        j_data = response.json()
        if j_data['authenticated']:
            for user_for_parse in self.user_for_parses:
                yield response.follow(
                    f'/{user_for_parse}',
                    callback=self.user_parse,
                    cb_kwargs={'username_for_parse': user_for_parse}  # протаскиваем дальше нужные данные
                )



    def user_parse(self, response: HtmlResponse, username_for_parse):
        ''' Собираем объект от куда будет производится парсинг  '''
        user_id_for_parse = self.fetch_user_id(response.text, username_for_parse) # В метод с регуляркой мы ложим страницу и имя пользователя
        followers = 'followers/?count=12' #   п о д п и с ч и  к и
        following = 'following/?count=12'
        user_info_url = f'{self.user_info_link.format(user_id_for_parse)}'
        start_followers_url = f'{self.subscriptions_link.format(user_id_for_parse)}{followers}'
        start_following_url = f'{self.subscriptions_link.format(user_id_for_parse)}{following}'

        yield response.follow(user_info_url,
                              callback=self.user_info_parse,
                              cb_kwargs={'username_for_parse': username_for_parse,
                                         'user_id_for_parse': user_id_for_parse}
                              )

        yield response.follow(start_following_url,
                              callback=self.user_following_parse,
                              cb_kwargs={'following': following,
                                         'user_id_for_parse': user_id_for_parse})

        yield response.follow(start_followers_url,
                              callback=self.user_followers_parse,
                              cb_kwargs={'followers': followers,
                                         'user_id_for_parse': user_id_for_parse})



    def user_info_parse(self, response: HtmlResponse, username_for_parse, user_id_for_parse):
        j_data = response.json()
        id_user_parse = user_id_for_parse
        username_for_parse = username_for_parse
        url_user_parse = response.url
        media_count_full_name_parse = j_data.get('user').get('media_count')
        business_count_name_parse = j_data.get('user').get('is_potential_business')

        item = InstaparserItem(
            id_user_parse=id_user_parse,
            username_for_parse=username_for_parse,
            url_user_parse=url_user_parse,
            media_count_full_name_parse=media_count_full_name_parse,
            business_count_name_parse=business_count_name_parse)
        yield item

    def user_following_parse(self, response: HtmlResponse, following, user_id_for_parse):
        j_data = response.json()
        list_following_users = []
        if j_data.get('big_list'):
            next_max_id = j_data.get('next_max_id')
            following_url = f'{self.subscriptions_link.format(user_id_for_parse)}{following}&max_id={next_max_id}'
            yield response.follow(following_url,
                                  callback=self.user_following_parse,
                                  cb_kwargs={'user_id_for_parse': user_id_for_parse,
                                             'following': following})

            following_users = j_data.get('users')

            for following_user in following_users:
                dict_following_user = {}
                dict_following_user['following_id'] = following_user.get('pk'),
                dict_following_user['following_username'] = following_user.get('username'),
                dict_following_user['following_full_name'] = following_user.get('full_name'),
                dict_following_user['following_profile_url'] = self.user_info_link.format(following_user.get('pk'))
                list_following_users.append(dict_following_user)

        item = InstaparserItem(list_following_users=list_following_users)
        yield item

    def user_followers_parse(self, response: HtmlResponse, followers, user_id_for_parse):
        j_data = response.json()
        list_followers_users = []
        if j_data.get('big_list'):
            next_max_id = j_data.get('next_max_id')
            followers_url = f'{self.subscriptions_link.format(user_id_for_parse)}{followers}&max_id={next_max_id}&amx_id={next_max_id}&search_surface=follow_list_page'
            yield response.follow(followers_url,
                                  callback=self.user_followers_parse,
                                  cb_kwargs={'user_id_for_parse': user_id_for_parse,
                                             'followers': followers})

            followers_users = j_data.get('users')
            for following_user in followers_users:
                dict_followers_user = {}
                dict_followers_user['followers_id'] = following_user.get('pk'),
                dict_followers_user['followers_username'] = following_user.get('username'),
                dict_followers_user['followers_full_name'] = following_user.get('full_name'),
                dict_followers_user['followers_profile_url'] = self.user_info_link.format(following_user.get('pk'))
                list_followers_users.append(dict_followers_user)

        item = InstaparserItem(list_followers_users=list_followers_users)
        yield item


    def fetch_csrf_token(self, text):
        ''' извлечение  csrf токена'''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        ''' извлекаем id из текста '''
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
            # == расшифовка re => {"id":"любые цифры","username":"наше искомое имя в переменной"} == источник => "owner":{"id":"7709057810","username":"techskills_2022"}
        ).group()
        return json.loads(matched).get('id')