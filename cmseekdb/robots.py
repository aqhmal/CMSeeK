#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

# Detect cms using robots.txt
# Rev 1
import re
import cmseekdb.basic as cmseek
def check(url, ua):
    robots = url + '/robots.txt'
    robots_source = cmseek.getsource(robots, ua)
    # print(robots_source[1])
    if robots_source[0] == '1' and robots_source[1] != '':
        # Check begins here
        robotstr = robots_source[1]
        hstring = robotstr # too lazy to rename variables from the copied part below '-'
        #### START DETECTION FROM HERE
        ## || <- if either of it matches cms detected
        ## :::: <- all the strings has to match (implemented to decrease false positives)
        hkeys = [
        'If the Joomla site is installed::::Disallow: /administrator/:-joom',
        'Allow: /core/*.css$||Disallow: /index.php/user/login/||Disallow: /web.config:-dru',
        'Disallow: /wp-admin/||Allow: /wp-admin/admin-ajax.php:-wp',
        'Disallow: /kernel/::::Disallow: /language/::::Disallow: /templates_c/:-xoops',
        'Disallow: /textpattern:-tpc',
        'Disallow: /sitecore||Disallow: /sitecore_files||Disallow: /sitecore modules:-score',
        'Disallow: /phpcms||robots.txt for PHPCMS:-phpc',
        'Disallow: /*mt-content*||Disallow: /mt-includes/:-moto',
        'Disallow: /jcmsplugin/:-jcms',
        'Disallow: /ip_cms/||ip_backend_frames.php||ip_backend_worker.php:-impage',
        'Disallow: /flex/tmp/||flex/Logs/:-flex',
        'Disallow: /e107_admin/||e107_handlers||e107_files/cache:-e107',
        'Disallow: /plus/ad_js.php||Disallow: /plus/erraddsave.php||Disallow: /plus/posttocar.php||Disallow: /plus/disdls.php||Disallow: /plus/mytag_js.php||Disallow: /plus/stow.php:-dede',
        'modules/contentbox/themes/:-cbox',
        'Disallow: /contao/:-contao',
        'Disallow: /concrete:-con5',
        'Disallow: /auth/cas::::Disallow: /auth/cas/callback:-dscrs',
        'uc_client::::uc_server::::forum.php?mod=redirect*:-discuz',
        'Disallow: /AfterbuySrcProxy.aspx||Disallow: /afterbuy.asmx||Disallow: /afterbuySrc.asmx:-abuy',
        'Disallow: /craft/:-craft',    # Chances of it being a falsepositive are higher than the chances of me doing something good with my life ;__;
        'Disallow: /app/::::Disallow: /store_closed.html:-csc',
        'Disallow: /*?cartcmd=*:-dweb',
        'Disallow: /epages/Site.admin/||Disallow: /epages/*:-epgs',
        'Disallow: /Mediatheque/:-ezpub',
        'robots.txt automaticaly generated by PrestaShop:-presta'
        ]
        for keyl in hkeys:
            if ':-' in keyl:
                det = keyl.split(':-')
                if '||' in det[0]:
                    idkwhat = det[0]
                    dets = idkwhat.split('||')
                    for d in dets:
                        if d in hstring:
                            return ['1', det[1]]
                elif '::::' in det[0]:
                    # yet again i know there can be a better way of doing it and feel free to correct it :)
                    and_chk = '0' # 0 = neutral, 1 = passed, 2 = failed
                    chks = det[0].split('::::')
                    for chk in chks:
                        if and_chk == '0' or and_chk == '1':
                            if chk in hstring:
                                and_chk = '1'
                            else:
                                and_chk = '2'
                        else:
                            and_chk = '2'
                    if and_chk == '1':
                        return ['1', det[1]]
                else:
                    if det[0] in hstring:
                        return ['1', det[1]]

        t3_regex = re.search(r'Sitemap: http(.*?)\?type=', robotstr)
        if t3_regex != None:
            return ['1', 'tp3']

        return ['0','']
    else:
        cmseek.error('robots.txt not found or empty!')
        return ['0','']
