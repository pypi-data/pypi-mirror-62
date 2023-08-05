import unittest
from morphling.input import Reader
from morphling.copy import Copy
from morphling.output import Writer


class TestCopyData(unittest.TestCase):
    def test_be_able_to_create_data_struct_from_intput_data(self):
        reader = Reader()
        writer = Writer()
        obj = Copy(reader, writer)
        obj.construct('test/input_file/basic_line')
        actual = obj.data
        self.assertEqual(
            actual,
            [
                [
                    '1079784248112951296',
                    'reply',
                    '@PNchP_ เสียจัยอะ เพื่อนงัย นี่เพื่อนเอง',
                    '2019-01-01 00:00:00',
                    '560',
                    'twitter',
                    '1904452146',
                    'หมีชมพู',
                ]
            ],
        )

    def test_ba_able_to_create_data_struct_when_there_are_space_between_message(self):
        reader = Reader()
        writer = Writer()
        obj = Copy(reader, writer)
        obj.construct('test/input_file/space_between_message')
        actual = obj.data
        self.assertEqual(
            actual,
            [
                [
                    '079784245067829254',
                    'tweet',
                    'Happy New Years 2019🎉🎉 นะคะทุกคน ปีนี้ก็ขอฝากตัวด้วยค่ะ!\nปีที่แล้วถ้าทำอะไรผิดพลาดหรือทำให้ไม่พอใจอะไรไปต้องขอโทษด้วยนะคะ🙏\nดีใจที่ได้รู้จักกับทุกคนค่ะ แล้วก็ขอบคุณที่มาเวิ่นเว้อด้วยกันนะคะ ดีใจมากเลย',
                    '2019-01-01 00:00:00',
                    '9857',
                    'twitter',
                    '2161099140',
                    '🎄FreSan☕59 days countdown to wmtsb3',
                ]
            ],
        )

    def test_be_able_to_create_data_when_there_is_comma_between_message(self):
        reader = Reader()
        writer = Writer()
        obj = Copy(reader, writer)
        obj.construct('test/input_file/comma_between_message')
        actual = obj.data
        self.assertEqual(
            actual,
            [
                [
                    '1079784248717070336',
                    'tweet',
                    'dear past ,\nthank you for all the lessons.\n\n.\n#HappyNewYear2019 https://t.co/LNIo1hGeoR',
                    '2019-01-01 00:00:00',
                    '5209',
                    'twitter',
                    '1192256738',
                    'Maink มองโลก',
                ]
            ],
        )

    def test_be_able_to_construct_when_owner_id_is_emoji(self):
        reader = Reader()
        writer = Writer()
        obj = Copy(reader, writer)
        obj.construct('test/input_file/owner_name_end_with_emoji')
        actual = obj.data
        self.assertEqual(
            actual,
            [
                [
                    '1079784244640010240',
                    'tweet',
                    'จุดพลุกันสนุกมากนะ',
                    '2019-01-01 00:00:00',
                    '9672',
                    'twitter',
                    '1013618778',
                    '💖',
                ]
            ],
        )

    def test_be_able_to_construct_data_when_owner_name_has_newline_in_between(self):
        reader = Reader()
        writer = Writer()
        obj = Copy(reader, writer)
        obj.construct('test/input_file/owner_name_has_new_line_in_between')
        actual = obj.data
        self.assertEqual(
            actual,
            [
                [
                    'skincarebymild__BuMRKW4FQyG',
                    'post',
                    'ตามหากันแดดอยู่มาทางนี้เด้อ💚\nกันแดดซันคิส หน้าเงา นักเรียนนักศึกษาใช้ทาไปโรงเรียนก็ได้ไม่วอก ทาได้ทุกสภาพผิว เกลี่ยง่าย เป็นกันแดดผสมโปรตีนไหมพร้อมบำรุงผิวหน้า spf50 pa+++ 🌤\n#ดีขนาดนี้ไม่ลองไม่ได้แล้ว .\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n.\n☀️สอบถาม | สั่งซื้อ | ปรึกษาฟรี🌵\n🌈Line ID : @zik7826z\n🍓หรือ ไดเรก ig\n#skincärebymild\n.\n.\n. .\n.\n.\n.\n.\n#ลิปมาร์ค #ราคานักเรียน #ราคานักเรียนนักศึกษา #บำรุงผิวหน้า #บำรุงปาก #laneige #สลิปปิ้งมาร์ค #ลาเนจของแท้ #ลาเนจ #ฉันจะสวย #ซันคิส #sunkiss',
                    '2019-02-23 00:01:13',
                    '8443',
                    'instagram',
                    '9188904578',
                    '♡𝑻𝒆𝒔𝒕𝒆𝒓 • 𝒍𝒂𝒏𝒆𝒊𝒈𝒆 • \n𝑺𝒖𝒏𝒌𝒊𝒔𝒔\n',
                ],
                [
                    '1079784248112951296',
                    'reply',
                    '@PNchP_ เสียจัยอะ เพื่อนงัย นี่เพื่อนเอง',
                    '2019-01-01 00:00:00',
                    '560',
                    'twitter',
                    '1904452146',
                    'หมีชมพู',
                ],
                [
                    'pcnk_2hand_Bvo-Iy3g7gw',
                    'post',
                    '🌻🌻🌻 เสื้อน่ารักผ้าใส่สบาย 50฿ . 📌 ✨ลทบ 30 ems 50\n✨เกงยีนส์ 40 ems 60\n\n__________________________\nกติกา📢📢📢 ‼️‼️ เอฟใต้รูป หรือทักหาแม่ค้าได้เลยน้าาา‼️‼️ ❌เอฟก่อนโอนก่อนส่งก่อน งดดราม่าจ้าาา❌ 🙏🏻พร้อมโอนค่อยทักมานะคะ ไม่เอฟเล่นน้าาา🙏🏻 #เสื้อผ้ามือสอง #โล๊ะตู้ #เสื้อผ้าแฟชั่น #เสื้อผ้า #โล๊ะตู้เสื้อผ้ามือสอง #ส่งต่อเสื้อผ้ามือสอง #โล๊ะตู้เสื้อผ้า #โล๊ะเสื้อผ้า #เสื้อผ้าสวยๆ #2hand #ส่งต่อสภาพนางฟ้า #ส่งต่อ #เสื้อผ้าถูกๆ #เสื้อผ้ามือ2 #เสื้อผ้าราคาถูก #เสื้อผ้าราคาถูกพร้อมส่ง #เสื้อผ้าราคาเบาๆ #สภาพนางฟ้า #มือสองสภาพดี #มือสองราคาถูก #กางเกง #วินเทจ #เกงยีนส์ #กางเกงถูกๆ #2hand  #2handthailand #มือสอง #วินเทจ #ราคาถูก #เสื้อผ้าน่ารัก',
                    '2019-03-31 00:04:21',
                    '3860',
                    'instagram',
                    '10677434124',
                    'HELLO 👋 \nเสื้อผ้ามือ 1,2👕👗\n',
                ],
                [
                    '1112038291539263489',
                    'tweet',
                    'ซื้อบัตร cat6 ดีม่ะ หรือจะเก็บเงินไปซื้อของ cat t-shirt',
                    '2019-03-31 00:06:04',
                    '315',
                    'twitter',
                    '267263658',
                    'มุกสุเตรียมขึ้นวอร์ดmed',
                ],
            ],
        )

    def test_be_able_to_construct_from_multiple_line(self):
        reader = Reader()
        writer = Writer()
        obj = Copy(reader, writer)
        obj.construct('test/input_file/multiple_line')
        actual = obj.data
        self.assertEqual(
            actual,
            [
                [
                    '1079784244640010240',
                    'tweet',
                    'จุดพลุกันสนุกมากนะ',
                    '2019-01-01 00:00:00',
                    '9672',
                    'twitter',
                    '1013618778',
                    '💖',
                ],
                [
                    '1079784248112951296',
                    'reply',
                    '@PNchP_ เสียจัยอะ เพื่อนงัย นี่เพื่อนเอง',
                    '2019-01-01 00:00:00',
                    '560',
                    'twitter',
                    '1904452146',
                    'หมีชมพู',
                ],
                [
                    '1079784248717070336',
                    'tweet',
                    'dear past ,\nthank you for all the lessons.\n\n.\n#HappyNewYear2019 https://t.co/LNIo1hGeoR',
                    '2019-01-01 00:00:00',
                    '5209',
                    'twitter',
                    '1192256738',
                    'Maink มองโลก',
                ],
                [
                    '2104171073012154_2104263833002878',
                    'comment',
                    '',
                    '2019-03-31 00:06:02',
                    '7434',
                    'facebook',
                    '00000000',
                    'Unknown',
                ],
                [
                    'kpw_VFen_oJpn_Bvo-',
                    'post',
                    '#KRISTPERAWATSKY\n••\n••\nCr. Twitter : niitnoii \nสามารถดูรูปเพิ่มได้ทีวิตเตอร์ชื่อนี้น้าา\n#kristtps #kristperawat\n#พลทหารของก้อน #thxpic #ยยขคพ',
                    '2019-03-31 00:06:02',
                    '1662',
                    'instagram',
                    '4484800865',
                    'kristtppraew_fc',
                ],
                [
                    'ultraviyolehi_Bvo-Qponcnp',
                    'post',
                    'Sen nasıl böyle yakışıklı oldun kolyeni yerim senin. Aşka geldim mdösmd\n\n#tawan_v #taytawan #newwiee #newthitipoom #taynew #petekao #OurSkyy #kissmeagain #darkbluekiss #TayNewMealDate #GMM25 #GMMTV #LineTV #bl #blseries #oishi #thaiseries #thaiboy #thaiactor #ฮันนี่ #polca #เตนิว #boyslove #cuteboys\n#taynew #taytawan  #newwietitiphoom  #kissmeagain #darkbluekiss #kristsingto #sotusstheseries  #addictedwebseries\n#addicted',
                    '2019-03-31 00:06:02',
                    '1630',
                    'instagram',
                    '11594034019',
                    'ultraviyolehi',
                ],
            ],
        )

    def test_be_able_to_construct_data_when_message_contain_datetime(self):
        reader = Reader()
        writer = Writer()
        obj = Copy(reader, writer)
        obj.construct('test/input_file/messge_contain_datetime')
        actual = obj.data
        self.assertEqual(
            actual,
            [
                [
                    '1079784250675613698',
                    'tweet',
                    '2019-01-01 00:00:01\n6. Chiang Rai\n7. #NHK紅白\n8. #ICONSIAM\n9. #อยากบอกอะไรygก่อนปีใหม่มั้ย\n10. #แผ่นดินไหว',
                    '2019-01-01 00:00:01',
                    '880',
                    'twitter',
                    '837126367779008512',
                    'TopTrendThai',
                ],
                [
                    '1108050502279819265',
                    'tweet',
                    '2019-03-20 00:00:00 6. toy story 4 7. Blind Trust 8. #ลดโลกเลอะกับผลิต 9. #จดหมายเด็กแมว 10. #OCLOCK',
                    '2019-03-20 00:00:00',
                    '4132',
                    'twitter',
                    '837126367779008512',
                    'TopTrendThai',
                ],
                [
                    '1108051014274314240',
                    'tweet',
                    'Rank 1 Youtube Trend 2019-03-20 00:02:01 เลิกคุยทั้งอำเภอเพื่อเธอคนเดียว - ลิลลี่ ได้หมดถ้าสดชื่น Feat.เก้า เกริกพล [OFFICIAL MV】',
                    '2019-03-20 00:02:03',
                    '8075',
                    'twitter',
                    '837126367779008512',
                    'TopTrendThai',
                ],
                [
                    '1102252313303904256',
                    'reply',
                    '@icez นิยายอัพเดท: Dreamcatcher : Corona Australis Academy (2019-03-03 23:59:14) https://t.co/7BUEIV1s2e',
                    '2019-03-04 00:00:05',
                    '2287',
                    'twitter',
                    '254500720',
                    'icez network',
                ],
                [
                    '1102614688255238144',
                    'tweet',
                    'Twitter Trend\n2019-03-05 00:00:01\n1. #thevoiceTH\n2. #กรงกรรม\n3. #จันทร์Shockโลกยังไงซิ\n4. #หัวใจศิลา\n5. #ดีใจด้วยนะ',
                    '2019-03-05 00:00:01',
                    '7406',
                    'twitter',
                    '837126367779008512',
                    'TopTrendThai',
                ],
                [
                    '38667962',
                    'post',
                    'ลง Skyrim ใน Steam ใหม่ เนื่องจากว่าอยู่ดีๆ ตัวเกมมันหายไป(ไม่ได้กด Uninstall เลย) และอยากกลับมาเล่นใหม่<br />\n<br />\nปรากฏว่า มันลงไม่ได้....และมันจะสุ่ม Error มา แต่ละครั้งจะไม่เหมือนกัน เช่น<br />\n<br />\nการอ่านดิสก์ผิดพลาด<br />\nดิสก์เสียหาย<br />\nไฟล์อัพเดตเสียหาย<br />\n<br />\n<img class="img-in-post" src="https://f.ptcdn.info/021/063/000/poirsfi8dCQ9zZa5TZW-o.png" data-image="img:544x139" /> <img class="img-in-post" src="https://f.ptcdn.info/021/063/000/poirsfudeCJ0LMlJDJ5-o.png" data-image="img:520x119" /> <img class="img-in-post" src="https://f.ptcdn.info/021/063/000/poirsf82a0yD1Uowr6G-o.png" data-image="img:492x125" /><br />\nจากนั้นก็ลอง....<br />\n<br />\n- ให้ Steam ตรวจสอบเกม<br />\n- ลบแล้วลงใหม่(ไม่ผ่านการให้ Steam ครวจสอบเกมแบบครั้งก่อน คือลงแบบ Clean เลย)<br />\n- ลบไฟล์ที่มีปัญหา ในที่นี้คือ dragonborn.bsa และ HighResTexturePack03.bsa ออก แล้วให้ Steam ครวจสอบไฟล์ใหม่<br />\n- ใช้คำสั่ง chkdsk แล้วกลับไปทำซ้ำข้อ 1-3<br />\n- ก็อปไฟล์ที่มันขึ้น Error จากอีกเครื่องมาลงทับ<br />\n- เอา Backup จากอีกเครื่องมาใส่<br />\n- ลบแคช<br />\n<br />\nลองทำหมดแล้วก็เหมือนเดิม<br />\n<br />\nเลยลองให้ Steam ซ่อมคลังเกมใหม่ดูและใช้คำสั่ง chkdsk ปรากฏว่ามันไม่มีอะไรผิดปกติเลย และไม่มีแจ้ง Error มาด้วย<br />\n<br />\n<img class="img-in-post" src="https://f.ptcdn.info/021/063/000/poirsfh0zyca8P6sUZ0-o.png" data-image="img:619x895" /> <img class="img-in-post" src="https://f.ptcdn.info/021/063/000/poirsfd93dhT857B5OZ-o.png" data-image="img:1333x625" /> <img class="img-in-post" src="https://f.ptcdn.info/021/063/000/poirsf3bxut0QpNcTSkE-o.png" data-image="img:1327x606" /><br />\nไฟล์ Log ใน Steam<br />\n<br />\n<img class="img-in-post" src="https://f.ptcdn.info/021/063/000/poirsgn22TFW18ynxbH-o.png" data-image="img:1791x469" /><br />\n<div class="code-style">[2019-03-17 22:36:26] Failed to write chunk in file <br />\n&quot;Data\\HighResTexturePack03.bsa&quot; 1048576 bytes at offset 1013856808 (Device Corrupt)</div><br />\nไม่ไหวแล้ว....ลองลักไก่ รันเกมโดยตรงจาก SkyrimLauncher.exe ก็ไม่ได้ มันบังคับอัพเดตแล้วก็แบบนี้<br />\n<br />\n<img class="img-in-post" src="https://f.ptcdn.info/021/063/000/poirx3oooWUW1SUS991-o.png" data-image="img:553x191" /><br />\nสรุปคือลองทุกอย่างแล้ว แล้วควรจะทำยังไงต่อดี??',
                    '2019-03-18 00:01:16',
                    '2344',
                    'pantip',
                    '663452',
                    'MrCatZaa',
                ],
            ],
        )

    def test_be_able_to_construct_data_when_owner_id_is_cha(self):
        reader = Reader()
        writer = Writer()
        obj = Copy(reader, writer)
        obj.construct('test/input_file/owner_id_is_cha')
        actual = obj.data
        self.assertEqual(
            actual,
            [
                [
                    'mifarashita_BsnYvqDhEKM_d1c6e9dd2f6e65209065b5bb7533b02ca0d0fe3d',
                    'comment',
                    '@pansika ขอบคุณค่าา😘',
                    '2019-01-15 00:02:15',
                    '4462',
                    'instagram',
                    'mifarashita',
                    'mifarashita',
                ],
            ],
        )

    def test_be_able_to_construct_data_from_csv_file(self):
        reader = Reader()
        writer = Writer()
        obj = Copy(reader, writer)
        obj.construct_csv('test/input_file/csv_format')
        actual = obj.data
        self.assertEqual(
            actual,
            [
                [
                    'id',
                    'type',
                    'message',
                    'time',
                    'engagement',
                    'channel',
                    'owner id',
                    'owner name',
                ],
                [
                    '1079784248717070336',
                    'tweet',
                    'dear past ,\nthank you for all the lessons.\n\n.\n#HappyNewYear2019 https://t.co/LNIo1hGeoR',
                    '2019-01-01 00:00:00',
                    '5209',
                    'twitter',
                    '1192256738',
                    'Maink มองโลก',
                ],
                [
                    '1079784281419862021',
                    'tweet',
                    '𝙃𝘼𝙋𝙋𝙔 𝙉𝙀𝙒 𝙔𝙀𝘼𝙍 𝟮𝟬𝟭𝟵 🌻💛\n𝑀𝑎𝑦 𝟤𝟢𝟣𝟫 𝑏𝑒 𝑡𝘩𝑒 𝑦𝑒𝑎𝑟 𝑤𝘩𝑒𝑛 𝑎𝑙𝑙 𝑦𝑜𝑢𝑟 𝑑𝑟𝑒𝑎𝑚𝑠 𝑐𝑜𝑚𝑒 𝑡𝑟𝑢𝑒, 𝑎𝑙𝑙 𝑦𝑜𝑢𝑟 𝘩𝑎𝑟𝑑 𝑤𝑜𝑟𝑘 𝑟𝑒𝑎𝑝 𝑔𝑟𝑒𝑎𝑡 𝑟𝑒𝑠𝑢𝑙𝑡𝑠 𝑎𝑛𝑑 𝑟𝑒𝑤𝑎𝑟𝑑𝑠. 𝐻𝑎𝑝𝑝𝑦 𝑁𝑒𝑤 𝑌𝑒𝑎𝑟. #JANUARYWISH https://t.co/wBHjlps4hQ',
                    '2019-01-01 00:00:08',
                    '4715',
                    'twitter',
                    '986274954030137344',
                    'ป้อกแป้ก',
                ],
            ],
        )

    def test_be_able_to_restruct_csv_data(self):
        reader = Reader()
        writer = Writer()
        obj = Copy(reader, writer)
        destination_source = 'test/output_file/csv_format.csv'
        obj.restruct_csv('test/input_file/csv_format', destination_source)
        with open(destination_source, 'r') as reader:
            actual = reader.read()
        self.assertEqual(
            'id,type,message,time,engagement,channel,owner id,owner name\n1079784248717070336,tweet,"dear past ,\nthank you for all the lessons.\n\n.\n#HappyNewYear2019 https://t.co/LNIo1hGeoR",2019-01-01 00:00:00,5209,twitter,1192256738,Maink มองโลก\n1079784281419862021,tweet,"𝙃𝘼𝙋𝙋𝙔 𝙉𝙀𝙒 𝙔𝙀𝘼𝙍 𝟮𝟬𝟭𝟵 🌻💛\n𝑀𝑎𝑦 𝟤𝟢𝟣𝟫 𝑏𝑒 𝑡𝘩𝑒 𝑦𝑒𝑎𝑟 𝑤𝘩𝑒𝑛 𝑎𝑙𝑙 𝑦𝑜𝑢𝑟 𝑑𝑟𝑒𝑎𝑚𝑠 𝑐𝑜𝑚𝑒 𝑡𝑟𝑢𝑒, 𝑎𝑙𝑙 𝑦𝑜𝑢𝑟 𝘩𝑎𝑟𝑑 𝑤𝑜𝑟𝑘 𝑟𝑒𝑎𝑝 𝑔𝑟𝑒𝑎𝑡 𝑟𝑒𝑠𝑢𝑙𝑡𝑠 𝑎𝑛𝑑 𝑟𝑒𝑤𝑎𝑟𝑑𝑠. 𝐻𝑎𝑝𝑝𝑦 𝑁𝑒𝑤 𝑌𝑒𝑎𝑟. #JANUARYWISH https://t.co/wBHjlps4hQ",2019-01-01 00:00:08,4715,twitter,986274954030137344,ป้อกแป้ก\n',
            actual,
        )

    def test_be_able_to_restruct_csv_file_when_owner_name_is_seperate_line(self):
        reader = Reader()
        writer = Writer()
        obj = Copy(reader, writer)
        destination_source = 'test/output_file/csv_owner_name_has_new_line_in_between.csv'
        obj.restruct_csv(
            'test/input_file/csv_owner_name_has_new_line_in_between', destination_source
        )
        with open(destination_source, 'r') as reader:
            actual = reader.read()
        self.assertEqual(
            'id,type,message,time,engagement,channel,owner id,owner name\n1079784248112951296,reply,@PNchP_ เสียจัยอะ เพื่อนงัย นี่เพื่อนเอง,2019-01-01 00:00:00,560,twitter,1904452146,หมีชมพู\npcnk_2hand_Bvo-Iy3g7gw,post,"🌻🌻🌻 เสื้อน่ารักผ้าใส่สบาย 50฿ . 📌 ✨ลทบ 30 ems 50\n✨เกงยีนส์ 40 ems 60\n\n__________________________\nกติกา📢📢📢 ‼️‼️ เอฟใต้รูป หรือทักหาแม่ค้าได้เลยน้าาา‼️‼️ ❌เอฟก่อนโอนก่อนส่งก่อน งดดราม่าจ้าาา❌ 🙏🏻พร้อมโอนค่อยทักมานะคะ ไม่เอฟเล่นน้าาา🙏🏻 #เสื้อผ้ามือสอง #โล๊ะตู้ #เสื้อผ้าแฟชั่น #เสื้อผ้า #โล๊ะตู้เสื้อผ้ามือสอง #ส่งต่อเสื้อผ้ามือสอง #โล๊ะตู้เสื้อผ้า #โล๊ะเสื้อผ้า #เสื้อผ้าสวยๆ #2hand #ส่งต่อสภาพนางฟ้า #ส่งต่อ #เสื้อผ้าถูกๆ #เสื้อผ้ามือ2 #เสื้อผ้าราคาถูก #เสื้อผ้าราคาถูกพร้อมส่ง #เสื้อผ้าราคาเบาๆ #สภาพนางฟ้า #มือสองสภาพดี #มือสองราคาถูก #กางเกง #วินเทจ #เกงยีนส์ #กางเกงถูกๆ #2hand  #2handthailand #มือสอง #วินเทจ #ราคาถูก #เสื้อผ้าน่ารัก",2019-03-31 00:04:21,3860,instagram,10677434124,"HELLO 👋 \nเสื้อผ้ามือ 1,2👕👗"\n1112038291539263489,tweet,ซื้อบัตร cat6 ดีม่ะ หรือจะเก็บเงินไปซื้อของ cat t-shirt,2019-03-31 00:06:04,315,twitter,267263658,มุกสุเตรียมขึ้นวอร์ดmed\n',
            actual,
        )

    def test_be_able_to_write_data_into_file_with_csv_format(self):
        reader = Reader()
        writer = Writer()
        obj = Copy(reader, writer)
        obj.construct('test/input_file/basic_line')
        output_path = 'test/output_file/basic_data_to_csv'
        obj.to_csv(output_path)
        with open(output_path, 'r') as reader:
            expect = reader.read()
        self.assertEqual(
            '1079784248112951296,reply,@PNchP_ เสียจัยอะ เพื่อนงัย นี่เพื่อนเอง,2019-01-01 00:00:00,560,twitter,1904452146,หมีชมพู\n',
            expect,
        )
