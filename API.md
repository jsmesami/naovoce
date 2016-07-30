FORMAT: 1A

HOST: https://na-ovoce.cz/api/v1

# Na ovoce API ver. 1.0

Na-ovoce.cz, public API

# Group Authorization Resource

## Obtain Token [POST https://na-ovoce.cz/api/v1/token/]

IMPORTANT: User registered with e-mail and password has to confirm her email address by
visiting a link that has been sent to her. Before that, she cannot obtain auth token.

+ Request (application/json)

        {
            "password": "123456",
            "username": "Ondra"
        }

+ Response 200

        {
            "token": "eb3e2b0367c2f99cf0380ef88127c2bf129c26a8",
            "id": 630
        }

## Obtain Token for existing Facebook account [POST https://na-ovoce.cz/api/v1/token/facebook/]

+ Request (application/json)

        {
            "email": "email@example.com",
            "fcb_id": "10204683629790171"
        }

+ Response 200

        {
            "token": "eb3e2b0367c2f99cf0380ef88127c2bf129c26a8",
            "id": 630
        }

# Group Sign Up Resource

## Sign Up With E-mail [POST https://na-ovoce.cz/api/v1/signup/]

IMPORTANT: User registered with this method has to verify her email address by visiting
a link that has been sent to her. Before that, she cannot be authenticated.

+ Request (application/json)

        {
            "email": "email@example.com",
            "username": "MasterPicker",
            "password": "letmein"
        }

+ Response 200

        {
            "id": 2066,
            "email": "email@example.com",
            "username": "MasterPicker"
        }

## Sign Up With Facebook [POST https://na-ovoce.cz/api/v1/signup/facebook/]

The client has to first obtain required user info (namely User Access Token) from Facebook.
Token obtained in response (along with user ID) can be used for further authentication.
This API endpoint can be used for both signing up and signing in.

+ Request (application/json)

        {
            "email": "email@example.com",
            "fcb_id": "10204683629790171",
            "fcb_token": "EAAGlZBTH339QBAFCy5N8JMeErVCMHI5sNNOxgk3rK9gh1WhM2pru8LdhS9..."
        }

+ Response 200

        {
            "token": "eb3e2b0367c2f99cf0380ef88127c2bf129c26a8",
            "id": 2067
        }

# Group Fruit Resource

## Fruit [https://na-ovoce.cz/api/v1/fruit/]

### List Fruit [GET https://na-ovoce.cz/api/v1/fruit/{?kind,user}]

+ Parameters
    + kind: `a1bb` (string, optional) - filters results by Kind (hex number)
    + user: `1093` (number, optional) - filters results by User (integer)

+ Response 200 (application/json)

        [
            {
                "id": 29549,
                "lat": "49.2586311000",
                "lng": "17.1221364000",
                "kind": "a412",
                "time": "2015-07-23 18:25:13",
                "url": "https://na-ovoce.cz/api/v1/fruit/29549/"
            },
            {
                "id": 29548,
                "lat": "50.7328562162",
                "lng": "15.1866808534",
                "kind": "a3c4",
                "time": "2015-07-23 11:05:03",
                "url": "https://na-ovoce.cz/api/v1/fruit/29548/"
            },
            {
                "id": 29547,
                "lat": "50.7330124016",
                "lng": "15.1861926913",
                "kind": "a3c4",
                "time": "2015-07-23 11:04:15",
                "url": "https://na-ovoce.cz/api/v1/fruit/29547/"
            },
            {
                "id": 29546,
                "lat": "49.2117829697",
                "lng": "16.6767632961",
                "kind": "a1e4",
                "time": "2015-07-23 08:59:10",
                "url": "https://na-ovoce.cz/api/v1/fruit/29546/"
            }
        ]

### Paginated Listing [GET https://na-ovoce.cz/api/v1/fruit/{?limit,offset}]

+ Parameters
    + limit: `2` (number, optional) - pagination limit (integer)
    + offset: `438` (number, optional) - pagination offset (integer)

+ Response 200 (application/json)

        {
            "count": 6132,
            "next": "https://na-ovoce.cz/api/v1/fruit/?limit=2&offset=440",
            "previous": "https://na-ovoce.cz/api/v1/fruit/?limit=2&offset=436",
            "results": [
                {
                    "id": 29167,
                    "lat": "50.1915997031",
                    "lng": "15.8397531509",
                    "kind": "a1d1",
                    "time": "2015-06-25 10:33:33",
                    "url": "https://na-ovoce.cz/api/v1/fruit/29167/"
                },
                {
                    "id": 29166,
                    "lat": "49.2059380091",
                    "lng": "16.6005536914",
                    "kind": "a3c4",
                    "time": "2015-06-11 15:55:35",
                    "url": "https://na-ovoce.cz/api/v1/fruit/29166/"
                }
            ]
        }

### Differences Listing [GET https://na-ovoce.cz/api/v1/fruit/since/{date}/{time}/]

+ Parameters
    + date: `2016-03-07` (string) - date since when you want the diff (YYYY-MM-DD)
    + time: `14:28:59` (string) - time since when you want the diff (hh:mm:ss)

+ Response 200 (applicetion/json)

        {
            "deleted": [
                {
                    "id": 32113,
                    "kind": "a0c9",
                    "time": "2016-03-07 13:21:38",
                    "url": "https://na-ovoce.cz/api/v1/fruit/32113/"
                },
                {
                    "id": 32110,
                    "kind": "a3a2",
                    "time": "2016-03-07 11:53:54",
                    "url": "https://na-ovoce.cz/api/v1/fruit/32110/"
                }
            ],
            "created": [
                {
                    "id": 32114,
                    "lat": "49.2067491593",
                    "lng": "16.6068064274",
                    "kind": "a0c9",
                    "time": "2016-03-07 13:27:55",
                    "url": "https://na-ovoce.cz/api/v1/fruit/32114/"
                },
                {
                    "id": 32112,
                    "lat": "49.1973823274",
                    "lng": "16.5835308945",
                    "kind": "a0c9",
                    "time": "2016-03-07 12:16:00",
                    "url": "https://na-ovoce.cz/api/v1/fruit/32112/"
                }
            ],
            "modified": []
        }


### Add Fruit [POST]

To create a POI. 
It takes a JSON object containing _location_, _kind_ and _description_ (optional) of the POI.
Response contains JSON payload with created object.

+ Authenticated

+ Request (application/json)

        {
            "lat": "50.0826536664",
            "lng": "14.4491297007",
            "kind": "a09b",
            "description": "Some description"
        }
    + Headers

        Authorization: Token eb3e2b0367c2f99cf0380ef88127c2bf129c26a8

+ Response 201 (application/json)

        {
            "id": 38104,
            "lat": "50.0826536664",
            "lng": "14.4491297007",
            "kind": "a09b",
            "time": "2016-01-01 00:43:02",
            "description": "Some description",
            "url": "https://na-ovoce.cz/api/v1/fruit/38104/",
            "user": {
                "id": 1093,
                "username": "veerruu",
                "url": "https://na-ovoce.cz/api/v1/users/1093/",
            }
        }

## Fruit Detail [https://na-ovoce.cz/api/v1/fruit/{fruit}/]

+ Parameters
    + fruit: `31980` (number) - ID of the Fruit (integer)

### View Fruit Detail [GET]

+ Response 200 (application/json)

        {
            "id": 31980,
            "lat": "50.295535106",
            "lng": "15.7891988754",
            "kind": "a1bb",
            "time": "2014-10-12 14:43:38",
            "url": "https://na-ovoce.cz/api/v1/fruit/31980/",
            "description": "Older Tree, Fruit too high.",
            "user": {
                "id": 1093,
                "username": "veerruu",
                "url": "https://na-ovoce.cz/api/v1/users/1093/"
            },
            "images_count": 0,
            "images": "https://na-ovoce.cz/api/v1/images/fruit/29626/"
        }

### Update Fruit [PATCH]

_Latitude_, _longitude_, _kind_ and _description_ can be updated.
Response contains JSON payload with updated object.

+ Authenticated and owner

+ Request (application/json)

        {
            "lat": "50.08268"
        }
    + Headers

        Authorization: Token eb3e2b0367c2f99cf0380ef88127c2bf129c26a8

+ Response 201 (application/json)

        {
            "id": 31980,
            "lat": "50.08268",
            "lng": "15.7891988754",
            "kind": "a1bb",
            "time": "2014-10-12 14:43:38",
            "url": "https://na-ovoce.cz/api/v1/fruit/31980/",
            "description": "Older Tree, Fruit too high.",
            "user": {
                "id": 1093,
                "username": "veerruu",
                "url": "https://na-ovoce.cz/api/v1/users/1093/"
            },
            "images": "https://na-ovoce.cz/api/v1/images/fruit/29626/"
        }

### Delete Fruit [DELETE]

Deleted fruit remains in the database. 
With `why_deleted` field you can specify the reason why you are deleting it.
You should encourage users to do so, although it's optional.
You can still GET the fruit to know the reason of deletion, 
but it no longer appears in listings.

+ Authenticated and owner

+ Request (application/json)

        {
            "why_deleted": "Cause I can."
        }
    + Headers

        Authorization: Token eb3e2b0367c2f99cf0380ef88127c2bf129c26a8

+ Response 204

### Send a Complaint [POST https://na-ovoce.cz/api/v1/fruit/{fruit}/complaint/]

To send a complaint on invalid Fruit marker.
Reason of complaint (`text` field) must be specified. 
Response contains JSON payload with created object.

+ Authenticated

+ Parameters
    + fruit: `31980` (number) - ID of the Fruit (integer)

+ Request (application/json)

        {
            "text": "I hereby make a complaint!"
        }
    + Headers

        Authorization: Token eb3e2b0367c2f99cf0380ef88127c2bf129c26a8

+ Response 201 (application/json)

        {
            "text": "I hereby make a complaint!"
        }

## Fruit Kinds [https://na-ovoce.cz/api/v1/fruit/kinds/]

### List Fruit Kinds [GET]

Language of the response depends on Accept-Language in the request header.
Available options are `cs` or `en`, `en` is default.

+ Request
    + Headers

            Accept-Language:en

+ Response 200 (application/json)

        [
            {
                "key": "a1e4",
                "name": "Apple Tree",
                "col": "E73932",
                "cls": "Trees"
            },
            {
                "key": "a09b",
                "name": "Chokeberry",
                "col": "21409A",
                "cls": "Trees"
            },
            {
                "key": "a1bb",
                "name": "Wild Garlic",
                "col": "669D24",
                "cls": "Bushes"
            }
        ]

# Group Users Resource

## Users [https://na-ovoce.cz/api/v1/users/]

### List Users [GET]

+ Response 200 (application/json)

        [
            {
                "id": 1093,
                "name": "veerruu",
                "url": "https://na-ovoce.cz/api/v1/users/1093/"
            },
            {
                "id": 1,
                "name": "Ondra",
                "url": "https://na-ovoce.cz/api/v1/users/1/"
            },
            {
                "id": 786,
                "name": "j.hofman",
                "url": "https://na-ovoce.cz/api/v1/users/786/"
            }
        ]

## User Detail [https://na-ovoce.cz/api/v1/users/{user}/]

+ Parameters
    + user: `1093` (number) - ID of the User (integer)

### View User Detail [GET]

+ Response 200 (application/json)

        {
            "id": 1093,
            "username": "veerruu",
            "url": "https://na-ovoce.cz/api/v1/users/1093/",
            "active": true,
            "fruit_count": 10,
            "fruit": "https://na-ovoce.cz/api/v1/fruit/?user=1093",
            "avatar": "https://secure.gravatar.com/avatar/361b7df6a40de3051439f645f54b7714?d=https%3A%2F%2Fna-ovoce.cz%2Fmedia%2Favatars%2F00001093-060-030.png&s=60",
            "motto": ""
        }

# Group Images Rersource

## Images [https://na-ovoce.cz/api/v1/images/]

### Delete Image [DELETE https://na-ovoce.cz/api/v1/images/{image}/]

+ Authenticated and owner

+ Parameters
    + image: `10384` (number) - ID of the Image (integer)

    + Headers

        Authorization: Token eb3e2b0367c2f99cf0380ef88127c2bf129c26a8

+ Response 204

### List Images of Fruit [GET https://na-ovoce.cz/api/v1/images/fruit/{fruit}/]

+ Parameters
    + fruit: `31980` (number) - ID of the Fruit (integer)

+ Response 200 (application/json)

        [
            {
                "id": 31980,
                "image": "https://na-ovoce.cz/api/gallery/fruit/29626/75626a6b7bc944679289d5ed52644572.png",
                "caption": "",
                "author": {
                    "id": 1,
                    "username": "Ondra",
                    "url": "https://na-ovoce.cz/api/v1/users/1/"
                }
            }
        ]

### Add Image to Fruit [POST https://na-ovoce.cz/api/v1/images/fruit/{fruit}/]

To add an Image associated to a Fruit.
It takes a JSON object containing base64-encoded _image data_ and _caption_.
Note: You do not have to send base64-encoded image data in JSON, 
`application/x-www-form-urlencoded` data is also supported.
Response contains JSON payload with created object.

+ Authenticated

+ Parameters
    + fruit: `31980` (number) - ID of the Fruit (integer)

+ Request (application/json)

        {
            "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAQDAwQDAwQEAwQFBAQFBgoHBgYGBg0JCggKDw0QEA8NDw4RExgUERIXEg4PFRwVF",
            "alt": "Look what I've found"
        }
    + Headers

        Authorization: Token eb3e2b0367c2f99cf0380ef88127c2bf129c26a8

+ Response 201 (application/json)

        {
            "id": 71,
            "image": "https://na-ovoce.cz/api/v1/images/fruit/29626/99b721aada344cff8abde88287e78083.png",
            "caption": "Look what I've found",
            "author": {
                "id": 1,
                "username": "Ondra",
                "url": "https://na-ovoce.cz/api/v1/api/v1/users/1/"
            }
        }

# Group Herbarium Resource

## Herbarium [https://na-ovoce.cz/api/v1/herbarium/]

### List Items [GET]

Description is HTML formatted.

+ Request (application/json)
    + Headers

            Accept-Language:en

+ Response 200 (application/json)

        [
            {
                "name": "Apricot Tree",
                "latin_name": "Prunus armeniaca",
                "description": "<p>Meruňka pochází z Číny. V našich končinách mnoho zástupců tohoto ovocného stromu nenajdeme. Meruňka vyžaduje teplejší podnebí, proto se s ní můžeme setkat spíše na jihu Moravy (odrůda Velkopavlovická) a v krajích, kde se daří vinné révě. </p>\n\n<p><strong>Identifikace:</strong> Strom dorůstá výšky 6&nbsp;m. Kvete ještě před olistěním. Jeho květy jsou bílé, lehce narůžovělé, rostou jednotlivě. Plody jsou kulaté, 4–8 cm velké peckovice s výrazným dělícím švem, pokožka drsná až sametová, zbarvená do žluta až oranžova, na straně přivrácené ke slunci může být načervenalá.</p>\n\n<p><strong>Užití:</strong> Plody se podobně jako ostatní plody rodu slivoní uplatňují při kompotování, výrobě džemů a marmelád, pečení buchet a koláčů, sušení či výrobě destilátů. U meruněk využíváme i jejich pecky, ze kterých se lisuje olej nebo se užívají jejich jadérka.</p>\n\n<p><strong>Léčitelství:</strong> Plody jsou velmi bohaté na vitamin A (proto oranžová barva) a draslík. Jsou oblíbeným pomocníkem při brzdění procesů stárnutí, regenerují buňky v našem těle. Podporují náš imunitní systém, slouží jako vysoký zdroj železa. Pecky meruněk by se neměly konzumovat ve větším množství. Malé množství má ale velmi pozitivní vliv na náš organismus, díky vitaminu B17 působí proti rakovině.</p>\n\n<p><strong>Kalendář sběru:</strong> červenec, srpen</p>\n",
                "photo": "http://127.0.0.1:9000/media/herbarium/merunka_2_UPR.jpg",
                "kind_key": "a13b"
            },
            {
                "name": "Yellow Plum",
                "latin_name": "Prunus domestica syriaca, Prunus domestica",
                "description": "<p>Tyto dva různé ovocné stromy u nás většinou označujeme pojmem „špendlík“, ve skutečnosti ale jde o různé poddruhy slivoně švestky, které se především liší barvou a dužninou plodu. U nás rostoucí mirabelka nancyská je odolní proti virovému onemocnění zvanému šárka a proto se vyskytuje častěji, než její příbuzný špendík.</p>\n\n<p><strong>Identifikace:</strong> Stromy jsou nižší, silně rozvětvené a rostou na světlých a teplých místech, často jsou vysázeny okolo venkovských cest, hojně je nalezneme i ve městech. Větve jsou bez trní. Plody mirabelky jsou sladké a aromatické, tvarem zakulacené a mají zlatožlutou barvu, kterou doplňuje ze strany, jež byla vystavena slunci, karmínové tečkování. Slupku lze jednoduše sloupnout. Naopak plody špendlíků jsou protáhlé, podobně jako u švestky, dužnina je měkká. Barva plodu je žlutá až oranžová. U obou druhů lze dužninu lehce oddělit od pecky.</p>\n\n<p><strong>Užití:</strong> Jak mirabelka, tak špendlík se pro svou sladkou aromatickou chuť hodí do koláčů, díky jemné kyselosti jsou výborné pro výrobu marmelád, džemů a povidel a kompotů. Vysoký obsah cukrů předurčuje jejich použití při pálení destilátů. </p>\n\n<p><strong>Léčitelství:</strong> Plodům špendlíků se někdy přezdívá „koště pro naše střeva“, jelikož jsou známy jejich projímavé účinky na zažívací ústrojí. Obsahují organické kyseliny, minerální látky a vitamíny.</p>\n\n<p><strong>Kalendář sběru:</strong> <br />\n Mirabelka – konec července <br />\n Špendlík – polovina srpna</p>\n",
                "photo": "http://127.0.0.1:9000/media/herbarium/mirabelka_UPR.jpg",
                "kind_key": "a1d1"
            },
        ]
