from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
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


def wait_and_perform_action(el: WebElement, function: str, argument: str, interval=2, retries=10):
    while retries:
        try:
            return getattr(el, function)(argument)
        except Exception:
            retries -= 1
            time.sleep(interval)


def log_in(driver: webdriver.Chrome, username, password):
    username_form = wait_and_perform_action(driver, 'find_element_by_name', 'username')
    slow_type(username_form, username)

    password_form = wait_and_perform_action(driver, 'find_element_by_name', 'password')
    slow_type(password_form, password)

    submit_btn = wait_and_perform_action(driver, 'find_element_by_xpath', '//button[@type="submit"]')
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
    
    posts = [{
        'url': a.get_attribute('href'),
        'preview': a.find_element_by_tag_name('img').get_attribute('src')
    } for a in posts_a]

    for idx, post in enumerate(posts):
        driver.get(post['url'])

        likes_views: WebElement = wait_and_perform_action(driver, 'find_element_by_xpath', '//section[2]/div')
        if 'views' in likes_views.text:
            likes_views.find_element_by_tag_name('span').click()
            likes_views = driver.find_element_by_xpath('//section[2]/div')
            posts[idx]['likes'] = ''.join(likes_views.text.split('\n')[1].split(' ')[0].split(','))
        else:
            posts[idx]['likes'] = ''.join(likes_views.text.split(' ')[0].split(','))

        print(post)
    return {'posts': posts}


def main(host_username='', host_password='', username='cristiano', mode='profile'):
    options = Options()
    # options.headless = True
    # options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    driver = webdriver.Chrome(options=options)

    driver.get('https://instagram.com')
    log_in(driver, host_username, host_password)

    # username = get_username(driver, user_id, host_username, host_password)
    # driver.get('https://instagram.com')

    driver.get(f'htps://instagram.com/{username}')

    avatar_url = wait_and_perform_action(driver, 'find_element_by_xpath', '//img').get_attribute('src')
    
    if mode == 'profile':
        data = get_profile_info(driver)
        
    elif mode == 'posts':
        data = get_posts(driver)

    else:
        raise NotImplementedError('The mode specified is not supported')

    # data['profile_id'] = user_id
    data['avatar_url'] = avatar_url

    driver.quit()

    return data


if __name__ == '__main__':
    data = main()
    print(data)