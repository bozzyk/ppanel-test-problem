import time
import sys
import logging
import json
import os
import platform

from typing import List
from random import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


logging.basicConfig(filename='log.txt', filemode='a', datefmt='%H:%M:%S', level=logging.DEBUG)

CHROME_OPTIONS = Options()
CHROME_OPTIONS.headless = True
CHROME_OPTIONS.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
CHROME_OPTIONS.add_argument('remote-debugging-port=9222')
CHROME_OPTIONS.add_argument("no-sandbox")
CHROME_OPTIONS.add_argument("window-size=1200x800")


def slow_type(element: WebElement, text: str):  # simulates input by human
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
    # driver is supposed to be at profile page
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
    
    logging.info(f'Profile info extracted: posts: {posts}, followers: {followers}, following: {following}')
    return {
        'posts': posts,
        'followers': followers,
        'following': following
    }


def scrap_post(driver, url):
    driver.get(url)
    likes = 0

    likes_views: WebElement = wait_and_perform_action(driver, 'find_element_by_xpath', '//section[2]/div')
    if not likes_views:
        return -1

    if 'views' in likes_views.text:
        likes_views.find_element_by_tag_name('span').click()
        likes_views = driver.find_element_by_xpath('//section[2]/div')
        likes = ''.join(likes_views.text.split('\n')[1].split(' ')[0].split(','))
    else:
        likes = ''.join(likes_views.text.split(' ')[0].split(','))

    return likes


def get_posts(driver, recent=False):
    # recent == true to take first 10 posts, otherwise - from 11th to 20th;
    posts_a: List[WebElement] = driver.find_elements_by_xpath('//article/div[1]/div/div/div/a')
    posts_a = posts_a[:10] if recent else posts_a[10:20]
    
    posts = [{
        'url': a.get_attribute('href'),
        'preview': a.find_element_by_tag_name('img').get_attribute('src'),
        'id': None
    } for a in posts_a]

    for idx, post in enumerate(posts):
        logging.info(f'Scrapping post with url = {post["url"]}')
        posts[idx]['likes'] = scrap_post(driver, post['url'])
        logging.info(f'Post likes: {posts[idx]["likes"]}')

    return {'posts': posts}


def main(host_username, host_password, username, mode='posts'):
    logging.info('Initializing webdriver')
    driver = webdriver.Chrome(options=CHROME_OPTIONS)

    driver.get('https://instagram.com')
    logging.info('Logging into instagram.com')
    log_in(driver, host_username, host_password)
    time.sleep(3)
    logging.info('Getting profile page')
    driver.get(f'https://instagram.com/{username}')

    try:
        avatar_url = wait_and_perform_action(driver, 'find_element_by_xpath', '//img').get_attribute('src')

    except NoSuchElementException:
        return dict()
    
    if mode == 'profile':
        logging.info(f'Getting profile info; username={username}')
        data = get_profile_info(driver)
        
    elif mode == 'posts':
        logging.info(f'Getting posts; username={username}')
        data = get_posts(driver)

    else:
        raise NotImplementedError('The mode "{mode}" specified is not supported')

    # data['profile_id'] = user_id
    data['avatar_url'] = avatar_url
    data['profile_id'] = None

    driver.quit()

    return data


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Credentials are missing; Usage: "python3 parser <username> <password> <target_username>"')
        exit()

    data = main(sys.argv[1], sys.argv[2], sys.argv[3])
    print(data)