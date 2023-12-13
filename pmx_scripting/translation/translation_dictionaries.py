from typing import Dict, List

"""
This file contains translation dictionaries that map Japanese words to English words.
Some are from PMXEditor built-in translation; Some are from Google Translate; Some are by. Nuthouse01
"""

katakana_half_to_full_dict = {
# dot
'･': '・',

# prolong
'ｰ': 'ー',

# aeiou big+small
'ｧ': 'ァ',
'ｨ': 'ィ',
'ｩ': 'ゥ',
'ｪ': 'ェ',
'ｫ': 'ォ',
'ｱ': 'ア',
'ｲ': 'イ',
'ｳ': 'ウ',
'ｴ': 'エ',
'ｵ': 'オ',

# ya yu yo tu small
'ｬ': 'ャ',
'ｭ': 'ュ',
'ｮ': 'ョ',
'ｯ': 'ッ',

# ya yu yo big
'ﾔ': 'ヤ',
'ﾕ': 'ユ',
'ﾖ': 'ヨ',

# pattern: x, x"
'ｶ': 'カ',
'ｶﾞ': 'ガ',
'ｷ': 'キ',
'ｷﾞ': 'ギ',
'ｸ': 'ク',
'ｸﾞ': 'グ',
'ｹ': 'ケ',
'ｹﾞ': 'ゲ',
'ｺ': 'コ',
'ｺﾞ': 'ゴ',
'ｻ': 'サ',
'ｻﾞ': 'ザ',
'ｼ': 'シ',
'ｼﾞ': 'ジ',
'ｽ': 'ス',
'ｽﾞ': 'ズ',
'ｾ': 'セ',
'ｾﾞ': 'ゼ',
'ｿ': 'ソ',
'ｿﾞ': 'ゾ',
'ﾀ': 'タ',
'ﾀﾞ': 'グ',
'ﾁ': 'チ',
'ﾁﾞ': 'ヂ',
'ﾂ': 'ツ',
'ﾂﾞ': 'ヅ',
'ﾃ': 'テ',
'ﾃﾞ': 'デ',
'ﾄ': 'ト',
'ﾄﾞ': 'ド',

# x, x", x*
'ﾊ': 'ハ',
'ﾊﾞ': 'バ',
'ﾊﾟ': 'パ',
'ﾋ': 'ヒ',
'ﾋﾞ': 'ビ',
'ﾋﾟ': 'ピ',
'ﾌ': 'フ',
'ﾌﾞ': 'ブ',
'ﾌﾟ': 'プ',
'ﾍ': 'ヘ',
'ﾍﾞ': 'ベ',
'ﾍﾟ': 'ペ',
'ﾎ': 'ホ',
'ﾎﾞ': 'ボ',
'ﾎﾟ': 'ポ',

# n sounds
'ﾅ': 'ナ',
'ﾆ': 'ニ',
'ﾇ': 'ヌ',
'ﾈ': 'ネ',
'ﾉ': 'ノ',

# m sounds
'ﾏ': 'マ',
'ﾐ': 'ミ',
'ﾑ': 'ム',
'ﾒ': 'メ',
'ﾓ': 'モ',

# r sounds
'ﾗ': 'ラ',
'ﾘ': 'リ',
'ﾙ': 'ル',
'ﾚ': 'レ',
'ﾛ': 'ロ',

# wa,wo,n,vu
'ﾜ': 'ワ',
'ﾜﾞ': 'ヷ',
'ｦ': 'ヲ',
'ｦﾞ': 'ヺ',
'ﾝ': 'ン',
'ｳﾞ': 'ヴ',

#### fullwidth wi,we have no halfwidth counterpart at all
# 30f0	30f0
# 30f1	30f1
'ヰﾞ': 'ヸ',
'ヱﾞ': 'ヹ',

# hiragana_small_to_big_dict
'ぁ': 'あ',  # a
'ぃ': 'い',  # i
'ぅ': 'う',  # u
'ぇ': 'え',  # e
'ぉ': 'お',  # o
}


# This dict is added to both "words" and "morphs"
symbols_dict = {
"×": "x",  # x0215 multiply symbol
"↑": "^^^", # x2191, NOTE: backslashes work poorly so /\ doesn't work right
"↓": "vvv", # x2193, NOTE: backslashes work poorly so \/ doesn't work right
"→": "->", # x2192
"←": "<-", # x2190
"ω": "w", # "omega"
"□": "box",  #x25a1
"■": "box",  #x25a0
"∧": "^",  #x2227 "logical and"
"▲": "^ open",  #x25b2
"△": "^ open",  #x25b3
"∨": "V",  #x2228 "logical or"
"▼": "V open",  #0x25bc
"▽": "V open",  #0x25bd
"∇": "V open",  #?
"★": "*",  #x2605
"☆": "*",  #x2606
"〜": "~",  # x301C wave dash, not a "fullwidth tilde" like in the "fullwidth_dict"
"○": "O",  #x25cb
"◯": "O",  #x25ef
"〇": "O",  # x3007
}


morph_dict = {
"ω□": "w open",  # without this entry it translates to "w box", and i dont like that
"まばたき": "blink",
"笑い": "laughing", # "warai" = laugh/laughing/laughter pmxe translates to "smile" but this is an eye morph
"ウィンク": "wink",
# "ウィンク右": "wink_R",  # not acutally possible cuz of pretranslate
"ウィンク2": "wink2",
"ウィンク右2": "wink2_R",
"ｳｨﾝｸ": "wink",
# "ｳｨﾝｸ右": "wink_R",  # not acutally possible cuz of pretranslate
"ｳｨﾝｸ2": "wink2",
"ｳｨﾝｸ右2": "wink2_R",
"ジト目": "doubt",
"じと目": "doubt",
"なごみ": "=.=", # "calm"
"びっくり": "surprise",
"驚き": "surprise",
"見開き": "wide eye",
"悲しい": "sad low",
"困る": "sadness",  # phonetically "komaru", google translates to "troubled", but PMXE translates to "sadness"... maybe "worried" is best?
"困った": "sadness",  # phonetically "komaru", same as above
"困り": "troubled",  # phonetically "komari"
"動揺": "upset",
"怒り": "anger",
"にこり": "cheerful",
"ｷﾘｯ": "serious eyes", # phonetically "kiri-tsu", might informally mean "confident"? kinda a meme phrase, a professional model translated this to 'serious' tho so idk
"キリッ": "serious eyes",  # same as above but full size
"星目": "star eyes",
"しいたけ": "star eyes", # "shiitake"
"ハート目": "heart eyes",
"ハート": "heart eyes",
"はぁと目": "heart eyes",
"はぁと": "heart eyes",
"ぐるぐる": "dizzy eyes", # perhaps "spinny"
"ぐる": "dizzy eyes", # perhaps "spinny"
"グルグル": "dizzy eyes", # perhaps "spinny"
"グル": "dizzy eyes", # perhaps "spinny"
"笑い目": "laughing eyes",
"カメラ目": "camera eyes", # for looking at the camera
"ｺｯﾁﾐﾝﾅ": "camera eyes",  # phonetically "Kotchiminna", might informally translate to "this guy" or "everyone" i guess? functionally same as "camera eyes" tho
"こっちみんな": "camera eyes", # phonetically "Kotchiminna", google translates to "don't look at me" maybe like "not my fault"?
"はぅ": ">.<",
"にやり": "grin",  # phonetically "niyari", not totally sure how this is different from "smile"
"ニヤリ": "grin",  # phonetically "niyari"
"にっこり": "smile",  # phonetically "nikkori"
"スマイル": "smile",  # phonetically "sumairu" aka engrish for "smile"
"ムッ": "upset",
"~": "wavy",
"照れ": "blush",  # "little blush", literally "shy"
"照れ2": "blush2",  # "big blush", literally "shy"
"照れ屋": "blush",  # another blush, literally "shy"
"赤面": "red face",  # literally "red face" but its just another blush
"青ざめる": "shock", # literally "aozomeru", translates to "pale", but the expression it represents is shock/horror
"青ざめ": "shock", # literally "aozame" translates to "pale", but the expression it represents is shock/horror
"丸目": "O.O",
"はちゅ目": "O.O",
"はちゅ目縦潰れ": "O.O height",
"はちゅ目横潰れ": "O.O width",
"ハイライト消し": "highlight off",
"瞳小": "scared", # "pupil"
"恐ろしい子!": "white eyes", # literally "scary child!" who the hell thought that was a good name?
"おそろしい子!": "white eyes", # phonetically the same as ^
"ぺろっ": "tongue out",  # phonetically "perrow"
"べー": "beeeeh", # another way of doing "tongue out" but google likes to turn this into 'base'
"あ": "A",
"い": "I",
"う": "U",
"え": "E",
"えー": "eeeeeh",  # long "e" sound
"お": "O",
"ワ": "Wa",
"ん": "N",  # default translation is "hmm" but this makes more sense I think? not commonly used anyway so w/e
"ふ": "F",  # uncommon
"ぴ": "P",  # uncommon
"上": "brow up", # "go up"
"下": "brow down", # "go down"
"前": "brow fwd",
"後": "brow back",
"涙": "tears",
}


# add the symbols into the morph dict
morph_dict.update(symbols_dict)


bone_dict =  {
"操作中心": "view cnt",
"全ての親": "motherbone",
"センター": "center",
"グルーブ": "groove",
"腰": "waist",
"足IK": "leg IK",
"つま先IK": "toe IK",
"上半身": "upper body",
"上半身2": "upper body2",
"下半身": "lower body",
"首": "neck",
"頭": "head",
"肩P": "shoulder_raise",  # "raise shoulder"
"肩": "shoulder",
"肩C": "shoulder_cancel",  # alternately "shoulder hidden"
"腕": "arm",
"腕IK": "armIK",
"腕捩": "arm twist",
"腕捩1": "arm twist1",  # "left arm rig1"
"腕捩2": "arm twist2",  # "left arm rig2"
"腕捩3": "arm twist3",  # "left arm rig3"
"ひじ": "elbow",
"手捩": "wrist twist",
"手捩1": "wrist twist1",  # "left elbow rig1"
"手捩2": "wrist twist2",  # "left elbow rig2"
"手捩3": "wrist twist3",  # "left elbow rig3"
"手首": "wrist",
"ダミー": "dummy",
"親指0": "thumb0",
"親指1": "thumb1",
"親指2": "thumb2",
"小指0": "little0",
"小指1": "little1",
"小指2": "little2",
"小指3": "little3",
"薬指0": "third0",
"薬指1": "third1",
"薬指2": "third2",
"薬指3": "third3",
"中指0": "middle0",
"中指1": "middle1",
"中指2": "middle2",
"中指3": "middle3",
"人指0": "fore0",
"人指1": "fore1",
"人指2": "fore2",
"人指3": "fore3",
"目": "eye",
"両目": "eyes",  # literally "both eyes"
"メガネ": "glasses",
"眼鏡": "glasses",
"腰キャンセル": "waist_cancel",
"足": "leg",  # standard leg-bones
"ひざ": "knee",
"足首": "foot",  # "ankle" is technically a more accurate translation but w/e this is standard name
"つま先": "toe",
"足D": "leg_D",      # "left/right thigh_D"
"ひざD": "knee_D",   # "left/right knee_D"
"足首D": "foot_D",   # "left/right foot_D"
"足先EX": "toe_EX", # "left/right toes_EX"
"胸": "breast",  # translates to "chest" or "breast"
"乳": "breast",  # translates to "breast" or "milk"??? idk man language is wierd
}


frame_dict = {
"センター": "Center",
"ＩＫ": "IK",
"IK": "IK",
"体(上)": "Upper Body",
"髪": "Hair",
"腕": "Arms",
"指": "Fingers",
"体(下)": "Lower Body",
"足": "Legs",
"つま先": "Toes",
"スカート": "Skirt",
"その他": "Other",
"物理": "Physics",
"物理-その他": "Physics - Other",
"その他-物理": "Other - Physics",
"服": "Clothes",
"胸": "Breasts",
"猫耳": "Nekomimi",
"ねこ耳": "Nekomimi",
"獣耳": "Kemonomimi",
"ケープ": "Cape",
"外套": "Mantle",
"握り・拡散": "Grip / Spread",
"握り-拡散": "Grip / Spread",
}


words_dict = {
# words
"操作中心": "view cnt",
"全ての親": "motherbone",
"モーフ": "morph",
"ネクタイ": "necktie",
"スカーフ": "scarf",
"マフラー": "scarf",  # actually "muffler" but a muffler is basically a scarf
"スカート": "skirt",
"ｽｶｰﾄ": "skirt",
"ﾄﾞﾚｽ": "dress",
"ドレス": "dress",
"リボン": "ribbon",
"ワンピース": "one-piece",  # as in a one-piece dress
"ニーソ": "knee socks",  # phonetically "niso", close enough i guess
"ピン": "pin",
"シャツ": "shirt",
"パンティー" : "panties",
"パンツ": "panties",
"ﾊﾟﾝﾂ": "panties",
"ぱんつ": "panties",
"ビキニ": "bikini",
"もみあげ": "sideburn",
"ｺｯﾁﾐﾝﾅ": "camera eyes",  # phonetically "Kotchiminna", might informally translate to "this guy" or "everyone" i guess? functionally same as "camera eyes" tho
"こっちみんな": "camera eyes",  # phonetically "Kotchiminna", google translates to "don't look at me" maybe like "not my fault"?
"尻尾": "tail",  # "shippo"
"しっぽ": "tail",  # "shippo"
"おっぱい": "boobs",  # literally "oppai"
"ヘッドセット": "headset",
"ヘッドホン": "headphone",  # phonetically "heddoHon"
"ヘッドフォン": "headphone",  # phonetically "heddoFon"
"センター": "center",
"グルーブ": "groove",
"上半身": "upper body",
"下半身": "lower body",
"タイツ": "tights",
"あほ毛": "ahoge",  # the cutesy little hair curl on top
"アホ毛": "ahoge",
"おさげ": "pigtail",
"お下げ": "pigtail",
"腰": "waist",
"舌": "tongue",
"胸": "breast",  # translates to "chest" or "breast"
"乳": "breast",  # translates to "breast" or "milk"??? idk man language is wierd
"乳首": "nipple",
"乳輪": "areola",
"ブラ": "bra",
"ブラジャー": "bra",
"耳": "ear",  # phonetically "mimi"
"みみ": "ear",  # phonetically "mimi"
"閉じ": "close",
"開く": "open",
"開け": "open",
"開き": "open",
"オープン": "open",  # phonetically "opun"
"髪の毛": "hair", # this literally means hair of hair??? odd
"毛": "hair",
"髪": "hair",
"髮": "hair", # this is actually somehow different from the line above???
"ヘアー": "hair",
"ヘア": "hair",
"新規": "new",
"材質": "material",
"尻": "butt",
"鎖": "chain",
"目": "eye",
"眼": "eye",
"瞳": "pupil",
"瞳孔": "pupil",
"着地": "landing",
"くぱ": "kupa",
"水着": "swimsuit",
"服": "clothes",
"着": "clothes",
"衣": "clothes",  # this one is chinese? maybe?
"ケープ": "cape",
"外套": "mantle",
"物理": "phys",
"カット": "cut",
"切る": "cut",
"飾り": "decoration", # either decoration or ornament
"補助": "helper",
"補正": "correction",
"ブロック": "block", # literally burroku, not sure why he picked this name
"花": "flower",
"鳥": "bird",
"弓": "bow",  # as archery bow not as in bending at the waist
"その他": "other",
"他": "other",
"ハイライト": "highlight",
"ﾊｲﾗｲﾄ": "highlight",
"艶": "gloss",
"靴下": "socks",
"靴": "shoes",  # phonetically "kutsu"
"くつ": "shoes",  # phonetically "kutsu"
"顔": "face",
"額": "forehead",
"ほほ": "cheek",  # phonetically "hoho"
"頬": "cheek",  # phonetically "hoho"
"あご": "chin",
"顎": "chin",
"足首": "foot",  # this must be high priority, otherwise its components will be individually (wrongly) translated
"手首": "wrist",  # this must be high priority, otherwise its components will be individually (wrongly) translated
"足": "leg",
"脚部": "leg",
"脚": "leg",
"腿": "thigh",  # phonetically "momo"
"もも": "thigh",  # phonetically "momo" but google thinks it means "peaches" lol
"手袋": "glove",
"グローブ": "glove",
"ベルト": "belt",
"手": "hand",
"首": "neck",
"親指": "thumb",
"人差指": "fore",
"人指": "fore",
"中指": "middle",
"薬指": "third",
"小指": "little",
"指": "finger",
"ひざ": "knee",
"膝": "knee",
"つま先": "toe",
"肩": "shoulder",
"腕": "arm",
"ひじ": "elbow",
"ヒジ": "elbow",
"腹黒": "dark",
"腹部": "abdomen",
"腹": "belly",
"頭": "head",
"帽子": "hat",
"金属": "metal",
"紐": "string",  # phonetically "himo", string or cord
"ひも": "string",  # phonetically "himo", string or cord
"ダミー": "dummy",
"ﾀﾞﾐ": "dummy",
"半": "half",
"身": "body",  # phonetically "mi"??? but it shows up in semistandard "upper body" name so w/e
"体": "body",  # phonetically "karada" lit. means body as in skin
"ボディ": "body",  # phonetically "bo di i" so it's pretty exact
"肌": "skin",
"裙": "skirt",  # chinese for "skirt"
"輪": "ring",  # was "round", better translation is ring/loop/circle maybe?
"武器": "weapon",
"ボタン": "button",  # phonetically "botan"
"釦": "button",  # phonetically "botan"
"連動": "interlock",
"捩": "twist",
"捻り": "twist",
"メガネ": "glasses",  # phonetically "megane"
"眼鏡": "glasses",  # phonetically "megane"
"星": "star",
"パーツ": "parts",
"筋": "muscle",
"帶": "band",
"そで": "sleeve",
"袖": "sleeve",
"歯": "teeth",
"牙": "fang",
"爪": "nail",
"犬": "dog",
"猫": "cat",  # phonetically "neko"
"ねこ": "cat",  # phonetically "neko"
"ネコ": "cat",  # phonetically "neko"
"バニー": "bunny",  # phonetically "ban ni"
"うさ耳": "rabbit ears",  # "usamimi"
"ウサギ": "rabbit",  # usagi
"獣": "animal",
"くち": "mouth",  # phonetically "kuchi"
"口": "mouth",  # phonetically "kuchi"
"唇": "lip",
"まぶた": "eyelid",  # phonetically "mabuta"
"瞼": "eyelid",  # phonetically "mabuta"
"まつげ": "eyelash",  # phonetically "matsuge"
"睫毛": "eyelash",  # phonetically "matsuge"
"睫": "eyelash",  # also somehow "matsuge"
"よだれ": "drool",
"まゆ": "brow",
"まゆ毛": "brow",
"眉毛": "brow",
"眉": "brow",
"発光": "glow",
"発": "emit",
"光": "light",
"かげ": "shadow",  # phonetically "kage"
"影": "shadow",  # phonetically "kage"
"鼻": "nose",
"表情": "expression",
"襟": "collar",  # phonetically "eri"
"頂点": "vertex",
"テクスチャ": "texture",
"骨": "bone",
"式": "model",
"甲": "armor",
"鎧": "armor",
"胴": "torso",
"マーク": "mark",
"ﾏｰｸ": "mark",
"ネック": "neck",
"ｽｰﾂ": "suit",
"スーツ": "suit",
"フード": "hood",  # phonetically "fudo" so it could mean "food" but more models will have sweatshirts with hoods than will have food
"支": "support",
"支え": "support",
"ちゃん": "-chan",  # for names
"さん": "-san",  # for names

# modifiers
"先": "end",
"親": "parent",
"中": "mid",
"右": "right",
"左": "left",
"上げ": "raise",  # motion
"下げ": "lower",  # motion
"上": "upper",  # relative position
"下": "lower",  # relative position
"前": "front",
"フロント": "front",
"後ろ": "back",  # not sure about this one
"背": "back",
"裏": "back",
"後": "rear",
"后": "rear",
"横": "side",  # or horizontal
"縦": "vert",
"両": "both",
"内": "inner",
"外": "outer",
"角": "corner",
"隅": "corner",
"法線": "normals",  # normals as in vertex normals not normal as in ordinary, i think?
"調整": "adjust",
"出し": "out",  # out as in takeout???
"全": "all",
"握り": "grip",
"握": "grip",
"拡散": "spread",
"拡": "spread",
"基部": "base",
"基礎": "base",  # more accurately "foundation" but this is shorter
"基": "base",  # either group or base
"錘": "weight",
"操作": "control",  # more closely translates to "operation" but w/e
"制御": "control",
"特殊": "special",

# morphs
"ジグザグ": "zigzag",
"ぺろっ": "tongue out",  # phonetically "perrow"
"べー": "beeeeh",  # another way of doing "tongue out"
"持ち": "hold",  # perhaps grab? holding? 手持ち = handheld
"ホールド": "hold",  # phonetically "horudo"
"ずらし": "shift",
"短": "short",
"長": "long",
"長い": "long",
"たれ": "drooping",  # "tare"
"タレ": "drooping",  # "tare"
"つり": "slanted",  # "tsuri"
"ツリ": "slanted",  # "tsuri"
"悔しい": "frustrated",  # "Kuyashī"
"穏やか": "calm",
"螺旋": "spiral",
"レイプ": "rape",  # "rape eyes" often mean "blank eyes"
"回転": "rotate",
"移動": "move",
"動": "motion",
"食込無": "none",
"無し": "none",
"無": "none",
"なし": "none",  # phonetically "nashi"
"ナシ": "none",  # phonetically "nashi"
"无": "none",
"消えて": "disappear", # as in whole model disappear
"消える": "disappear",
"透明": "transparent",
"透過": "transparent",
"広げ": "wide", # literally "spread"
"広い": "wide",
"広": "wide",
"潰れ": "shrink",  # literally "collapse"
"狭く": "narrow",
"狭": "narrow",
"幅": "width",
"細い": "thin",
"細": "thin",  # literally "fine"
"平行": "parallel",  # phonetically "hey ko"
"太": "thick",
"粗": "coarse",
"逆": "reverse",
"大": "big",
"巨": "big",
"暗い": "dark",
"暗": "dark",
"青ざめる": "shock", # literally "aozomeru", translates to "pale", but the expression it represents is shock/horror
"青ざめ": "shock", # literally "aozame" translates to "pale", but the expression it represents is shock/horror
"を隠す": "hide",
"非表示": "hide",
"追従": "follow",
"まばたき": "blink",
"笑い": "laughing",
"ウィンク": "wink",
"ウインク": "wink",  # this is somehow different than above?
"ｳｨﾝｸ": "wink",
"睨み": "glare",
"ｷﾘｯ": "serious", # phonetically "kiri-tsu", might informally mean "confident"? kinda a meme phrase, a professional model translated this to 'serious' tho so idk
"キリッ": "serious",  # same as above but full size
"ジト": "doubt", # jito
"じと": "doubt", # jito
"じど": "doubt", # jido but close enough that it probably means jito
"なごみ": "=.=", # "calm"
"びっくり": "surprise",
"驚き": "surprise",
"見開き": "spread",  # something closer to "wide eyes" but google says it's "spread" so idk
"悲しい": "sad low",
"困る": "sadness",  # phonetically "komaru", google translates to "troubled", but PMXE translates to "sadness"... maybe "worried" is best?
"困った": "sadness",  # phonetically "komaru", same as above
"困り": "troubled",  # phonetically "komari"
"真面目": "serious",  # has the symbol for "eye" but is actually a brow morph, odd
"真面": "serious",
"怒り": "anger",
"怒": "anger",
"にこり": "cheerful",
"しいたけ": "star", # "shiitake"
"ハート": "heart",
"はぁと": "heart",
"ぐるぐる": "dizzy", # perhaps "spinny"
"ぐる": "dizzy", # perhaps "spinny"
"グルグル": "dizzy", # perhaps "spinny"
"グル": "dizzy", # perhaps "spinny"
"カメラ": "camera", # for looking at the camera
"はぅ": ">.<",
"にやり": "grin",
"ニヤリ": "grin",  # these 2 are phonetically the same, "niyari"
"にっこり": "smile",
"キッス": "kiss",
"ムッ": "upset",
"照れ": "blush",
"赤面": "red face",
"黒": "black",
"白": "white",
"緑": "green",
"ピンク": "pink",
"黄": "yellow",
"紫": "purple",
"赤": "red",
"青": "blue",  # "ao", regular blue
"蒼": "blue",  # "ao", regular blue
"紺": "navy blue",  # "kon", technically "navy blue" but w/e
"金": "gold",
"銀": "silver",
"色": "color",
"汗": "sweat",
"円": "circle",
"表": "front", # not sure about this one, front as in outward-facing geometry, opposite of backward-facing geometry. literally means "table" tho lol
"縁": "edge",
"エッジ": "edge",
"丸い": "round",
"丸": "round",
"はちゅ": "round",
"縮": "shrink",
"小さく": "small",
"小": "small",
"消し": "erase",
"けし": "erase",
"消": "erase",
"裸": "bare", # or "naked" like bare legs
"あ": "a",  # hiragana a
"ア": "a",  # not one of the primary phonetic morphs, but shows up such as in "ワアアア" = "wa a a a"
"い": "i",  # hiragana i
"う": "u",  # hiragana u
"え": "e",  # hiragana e
"お": "o",  # hiragana o
"ワ": "wa",
"わ": "wa",  # not one of the primary phonetic morphs
"ん": "n",
"ふ": "f",  # uncommon
"ぴ": "p",  # uncommon
"なみだ": "tears",  # phonetically "namida"
"涙": "tears",  # phonetically "namida"
"へ": "eeeh",
"の": "of", # backwards yoda-style grammar: technically "A の B" translates to "B of A" but I can't do that switcheroo without major changes
"用": "for",  # backwards yoda-style grammar: same
"ー": "--", # not sure what to do with this, often used to mean continuation of a sound/syllable...
}


# add the special symbols
words_dict.update(symbols_dict)


prefix_dict = {
"中": "_M",
"右": "_R",
"左": "_L",
"親": " parent",
"先": " end",
}


odd_punctuation_dict = {
"’": "'",  # x2019
"╱": "/",  # x2571 "box drawing" section.
"╲": "\\",  # x2572 "box drawing" section. NOTE backslash isn't MMD friendly, find something better!
"╳": "X",  # x2573 "box drawing" section.
"　": " ",  # x3000, just a fullwidth space aka "ideographic space"
"、": ",",  # x3001, some sorta fullwidth comma
"。": ".",  # x3002
"〈": "<",  # x3008
"〉": ">",  # x3009
"《": "<",  # x300a
"》": ">",  # x300b
"「": '"',  # x300c
"」": '"',  # x300d
"『": '"', # x300e
"』": '"', # x300f
"【": "[",  # x3010
"】": "]",  # x3011
"〔": "[",  # x3014
"〕": "]",  # x3015
"〖": "[",  # x3016
"〗": "]",  # x3017
"〘": "[",  # x3018
"〙": "]",  # x3019
"〚": "[",  # x301a
"〛": "]",  # x301b
"・": "-",  # x30fb, could map to 00B7 but i don't think MMD would display that either
"〜": "~",  # x301C wave dash, not a "fullwidth tilde"
"｟": "(",  # xff5f
"｠": ")",  # xff60
"｡": ".",  #xff61
"｢": '"',  # xff62
"｣": '"',  # xff63
"､": ",",  # xff64
"･": "-",  # xff65
}


# https://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms_(Unicode_block)
ascii_full_to_basic_dict = {
	'！': '!', '＂': '"', '＃': '#', '＄': '$', '％': '%', '＆': '&', '＇': "'", '（': '(', '）': ')', '＊': '*',
	'＋': '+', '，': ',', '－': '-', '．': '.', '／': '/', '０': '0', '１': '1', '２': '2', '３': '3', '４': '4',
	'５': '5', '６': '6', '７': '7', '８': '8', '９': '9', '：': ':', '；': ';', '＜': '<', '＝': '=', '＞': '>',
	'？': '?', '＠': '@', 'Ａ': 'A', 'Ｂ': 'B', 'Ｃ': 'C', 'Ｄ': 'D', 'Ｅ': 'E', 'Ｆ': 'F', 'Ｇ': 'G', 'Ｈ': 'H',
	'Ｉ': 'I', 'Ｊ': 'J', 'Ｋ': 'K', 'Ｌ': 'L', 'Ｍ': 'M', 'Ｎ': 'N', 'Ｏ': 'O', 'Ｐ': 'P', 'Ｑ': 'Q', 'Ｒ': 'R',
	'Ｓ': 'S', 'Ｔ': 'T', 'Ｕ': 'U', 'Ｖ': 'V', 'Ｗ': 'W', 'Ｘ': 'X', 'Ｙ': 'Y', 'Ｚ': 'Z', '［': '[', '＼': '\\',
	'］': ']', '＾': '^', '＿': '_', '｀': '`', 'ａ': 'a', 'ｂ': 'b', 'ｃ': 'c', 'ｄ': 'd', 'ｅ': 'e', 'ｆ': 'f',
	'ｇ': 'g', 'ｈ': 'h', 'ｉ': 'i', 'ｊ': 'j', 'ｋ': 'k', 'ｌ': 'l', 'ｍ': 'm', 'ｎ': 'n', 'ｏ': 'o', 'ｐ': 'p',
	'ｑ': 'q', 'ｒ': 'r', 'ｓ': 's', 'ｔ': 't', 'ｕ': 'u', 'ｖ': 'v', 'ｗ': 'w', 'ｘ': 'x', 'ｙ': 'y', 'ｚ': 'z',
	'｛': '{', '｜': '|', '｝': '}', '～': '~',
}


# ===== Utils =====


def sort_dict_with_longest_keys_first(dictionary:Dict[str,str]) -> Dict[str,str]:
	L_D = [tuple(x) for x in dictionary.items()]
	L_D.sort(reverse=True, key=lambda x: len(x[0]))

	return dict(L_D)

def invert_dict(dictionary:Dict[str,str]) -> Dict[str,str]:
	inv = {v: k for k, v in dictionary.items()}

	return inv

def piecewise(in_list: List[str], in_dict: Dict[str, str]) -> list:
	outlist = []  # list to build & return

	dictitems = list(in_dict.items())

	for out in in_list:
		if (not out) or out.isspace():  # support bad/missing data
			outlist.append("JP_NULL")
			continue

		# goal: substrings that match keys of "words_dict" get replaced
		# starting from each char position, try to match against the contents of the dict. longest items are first!
		i = 0
		while i < len(out):  # starting from each char of the string,
			found_match = False

			for (key, val) in dictitems:  # try to find anything in the dict to match against,
				if out.startswith(key, i):  # and if something is found starting from 'i',
					found_match = True

					# i am going to replace it key->val
					out = out[0:i] + val + out[i + len(key):]

					# i don't need to examine or try to replace on any of these chars, so skip ahead a bit
					i += len(val)

					# nothing else will match here, since I just replaced the thing, so break out of iterating on dict keys
					break

			if found_match is False:
				i += 1

		# once all uses of all keys have been replaced, then append the result
		outlist.append(out)

	return outlist

def consolidate_dict_keys(D: Dict[str, str], consolidate: Dict[str, str]) -> Dict[str, str]:
	"""
	Use dict "consolidate" to modify the KEYS of D. If a key in D is changed,
	but the new key also existed in that dict, that is a "collision."
	If the old key's value and the existing key's value are the same, there's no problem.
	If they are different, then print a warning because it's a problem that needs to be manually resolved.
	"""

	newdict = {}
	keys = list(D.keys())
	values = list(D.values())

	# translate all the halfwidth chars to their fullwidth forms
	keys_full = piecewise(keys, consolidate)
	for K, KF, V in zip(keys, keys_full, values):
		if K == KF:
			# K did not contain any halfwitdth stuff, no change
			newdict[K] = V

		else:
			# K did contain halfwidth stuff and did change
			newdict[KF] = V

			# if KF was already in the dict, and KF has a different value than K, then we've got a problem
			# if KF was already in the dict but it had the same value as K, then there's no problem
			# print("'%s' -> '%s'" % (K, KF))
			if KF in keys and D[K] != D[KF]:
				print("key consolidation conflict! key='%s' value**='%s', key_new='%s' value_new='%s'" % (K, D[K], KF, D[KF]))

	return newdict


# ===== Set Up =====


katakana_half_to_full_dict = sort_dict_with_longest_keys_first(katakana_half_to_full_dict)
ascii_full_to_basic_dict = sort_dict_with_longest_keys_first(ascii_full_to_basic_dict)

words_dict = sort_dict_with_longest_keys_first(words_dict)
words_dict = consolidate_dict_keys(words_dict, ascii_full_to_basic_dict)
words_dict = consolidate_dict_keys(words_dict, katakana_half_to_full_dict)

morph_dict = sort_dict_with_longest_keys_first(morph_dict)
morph_dict = consolidate_dict_keys(morph_dict, ascii_full_to_basic_dict)
morph_dict = consolidate_dict_keys(morph_dict, katakana_half_to_full_dict)

bone_dict = sort_dict_with_longest_keys_first(bone_dict)
bone_dict = consolidate_dict_keys(bone_dict, ascii_full_to_basic_dict)
bone_dict = consolidate_dict_keys(bone_dict, katakana_half_to_full_dict)

frame_dict = sort_dict_with_longest_keys_first(frame_dict)
frame_dict = consolidate_dict_keys(frame_dict, ascii_full_to_basic_dict)
frame_dict = consolidate_dict_keys(frame_dict, katakana_half_to_full_dict)
