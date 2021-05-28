from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from random import random
from functools import partial
import time
import sys
import logging
import requests
import json


def slow_type(element: WebElement, text: str):
    for char in text:
        element.send_keys(char)
        time.sleep(random() * 0.3)  # reducing interval returned by random() from [0, 1) to [0, 0.3)


def get_username(driver: webdriver.Chrome, user_id, username, password):
    driver.get('https://commentpicker.com/instagram-username.php')
    input_form = driver.find_element_by_id('instagram-userid')
    slow_type(input_form, str(user_id))

    submit_btn : WebElement = driver.find_element_by_id('get-username-button')
    submit_btn.click()

    time.sleep(3)

    link_div : WebElement = driver.find_element_by_id('comment_users')
    url = link_div.find_element_by_tag_name('a').get_attribute('href')

    driver.get(url)
    data = json.loads(driver.find_element_by_tag_name('pre').text)
    
    return data['data']['user']['reel']['user']['username']


def log_in(driver: webdriver.Chrome, username, password):
    username_form = driver.find_element_by_name('username')
    slow_type(username_form, username)

    password_form = driver.find_element_by_name('password')
    slow_type(password_form, password)

    submit_btn = driver.find_element_by_xpath('//button[@type="submit"]')
    submit_btn.click()


def get_profile_info(driver: webdriver.Chrome):
    ''' driver is supposed to be at profile page'''
    def parse_custom_int(x):
        return int(''.join(x.split(',')))

    account_info_numerical : List[WebElement] = driver.find_element_by_tag_name('header').find_elements_by_tag_name('li')
    posts, followers, following = 0, 0, 0
    for item in account_info_numerical:
        if 'posts' in item.text:
            posts = parse_custom_int(item.find_element_by_xpath('span/span').text)
        elif 'followers' in item.text:
            followers = parse_custom_int(item.find_element_by_xpath('a/span').get_attribute('title'))
        elif 'following' in item.text:
            following = parse_custom_int(item.find_element_by_xpath('a/span').text)

    return {
        'posts': posts,
        'followers': followers,
        'following': following
    }


def get_posts(driver: webdriver.Chrome, recent=False):
    '''
        recent == true to take first 10 posts, otherwise - from 11th to 20th;
        driver is supposed to be at profile page
    '''
    posts_a: List[WebElement] = driver.find_elements_by_xpath('//article/div[1]/div/div/div/a')
    posts_a = posts_a[:10] if recent else posts_a[10:20]
    posts = list()
    for a in posts_a:
        post = {
            'url': a.get_attribute('href'),
            'preview': a.find_element_by_tag_name('img').get_attribute('src'),
            }
        a.click()
        time.sleep(1.5)

        likes_views: WebElement = driver.find_element_by_xpath('//section[2]/div')
        if 'views' in likes_views.text:
            likes_views.find_element_by_tag_name('span').click()
            likes_views = driver.find_element_by_xpath('//section[2]/div')
            post['likes'] = ''.join(likes_views.text.split('\n')[1].split(' ')[0].split(','))
        else:
            post['likes'] = ''.join(likes_views.text.split(' ')[0].split(','))

        post['likes'] = ''.join(driver.find_element_by_xpath('//section[2]/div/div/a/span').text.split(','))
        driver.find_element_by_xpath('/html/body/div[last()]/div[last()]/button').click()

        posts.append(post)
    return posts


def main(username='bozzyk44', password='Bozzyk311)@)*', user_id='173560420', mode='profile'):
    options = Options()
    # options.headless = True
    # options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    driver = webdriver.Chrome(options=options)

    driver.get('https://instagram.com')
    time.sleep(1)
    log_in(driver, username, password)
    time.sleep(4)

    target_username = get_username(driver, user_id, username, password)
    driver.get('https://instagram.com')

    if 'accounts/onetap/' in driver.current_url:  # case when instagram asks about saving Login info
        not_now_btn = filter(lambda x: x.text == 'Not Now', driver.find_elements_by_tag_name('button')).__next__().click()
        time.sleep(1)

    notifications_btn : List[WebElement] = list(filter(lambda x: x.text == 'Not Now', driver.find_elements_by_tag_name('button')))
    if notifications_btn:
        notifications_btn[0].click()
        time.sleep(1)

    search_field : WebElement = driver.find_element_by_xpath('//input[@placeholder="Search"]')
    slow_type(search_field, target_username)
    time.sleep(1)
    user_field : WebElement = driver.find_element_by_xpath('//div[text() = "cristiano"]')
    user_field.click()
    time.sleep(1)

    avatar_url = driver.find_element_by_xpath('//img').get_attribute('src')
    
    if mode == 'profile':
        data = get_profile_info(driver)
        
    elif mode == 'posts':
        data = get_posts(driver)

    else:
        raise NotImplementedError('The mode specified is not supported')

    data['profile_id'] = user_id
    data['avatar_url'] = avatar_url

    driver.quit()

    return data


if __name__ == '__main__':
    data = main()
    print(data)