from tests import url_checker


def test_reply() -> None:
    test_suffix_for_caching = "reply"
    url = "https://www.reddit.com/r/singapore/comments/1o5i3fl/contract_for_marine_parade_free_shuttle_bus/nj9fl4g/"
    expected_post = 'Better to end the operation then to let the public find out how much it cost.<br>Some friends of PAP sure benefit from this "free" shuttle bus service.<br>They could be charging 10k per trip.<br>Even better, like LBW. Oweself award ownself the tender.'  # noqa: E501
    expected_credit = (
        "2025 Oct 13, "
        "u/ValentinoCappuccino. "
        "r/singapore, "
        '"Contract for Marine Parade free shuttle bus service set to end". '
        f"{url}"
    )

    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )


def test_main_post() -> None:
    test_suffix_for_caching = "main_post"
    url = "https://www.reddit.com/r/singapore/comments/1oixj70/hsa_blood_stocklevels_for_a_is_critical_low_29_oct/"
    expected_post = "HSA Blood StockLevels for A- is Critical Low (29 Oct)<br>According to Red Cross Singapore website. The blood stock levels for A- is at critical low. Screenshot from Red Cross SG website.<br>As a regular blood donor, I hope people who are young and healthy and able to give. Please do so, and especially you are A negative.<br>Blood is needed to save lives in times of emergencies and to sustain the lives of those with medical conditions, like leukemia, thalassaemia and bleeding disorders, as well as patients who are undergoing major surgeries.<br>For many patients, blood donors are their lifeline. One unit of blood can save three lives!<br>Blood Stock level: https://redcross.sg/#bloodstock"  # noqa: E501
    expected_credit = (
        "2025 Oct 29, "
        "u/Bitter-Rattata. "
        "r/singapore, "
        '"HSA Blood StockLevels for A- is Critical Low (29 Oct)". '
        f"{url}"
    )

    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )


def test_backslash_n_replaced_with_br() -> None:
    test_suffix_for_caching = "blackslash_n_replaced_with_br"
    url = "https://www.reddit.com/r/singapore/comments/1o8rpju/grandpas_struggle_to_secure_a_better_hdb_flat/"
    expected_post = "Grandpa's struggle to secure a better HDB flat, 1970s<br>These are all the letters and forms kept by my maternal grandparents to get a HDB flat in the 70s.<br>My maternal grandfather or gua gong, was a coconut hawker with his wife in the old Tekka Market. Everyday, they opened early in the morning to serve the early morning customers, like cooked food hawkers who served breakfast and housewives. They would cut coconuts, grind coconuts and deliver coconuts to the old shophouses along the Rochor Canal.<br>They closed late at night around 10pm, after disposing of the coconut shells and other trash. It was very tiring work that made them desire to live near the market.<br>Originally, my gua gong, gua ma, my mother and her 4 siblings all lived at 12 Race Course Rd, which is now Exit E of the MRT here. My gua gong, who was born in poverty in China, was adopted by his Chia relatives here, who were abusive to him and his family. My own mother recounts being sent to become essentially their maid as a little girl. He wanted to get away from them, and got a 1 rm flat in Kim Keat. It was quickly realised to be too small for a family of 7  so he kept writing to the gov for a larger flat, or one closer to Tekka.<br>He secured Blk 422 AMK in 78 or 79, after years of trying, before selling that flat to finance his final home in Tekka, where I found his documents in our old furniture."  # noqa: E501
    expected_credit = (
        "2025 Oct 17, "
        "u/mt-tekka. "
        "r/singapore, "
        '"Grandpa\'s struggle to secure a better HDB flat, 1970s". '
        f"{url}"
    )

    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )


def test_deleted_user() -> None:
    test_suffix_for_caching = "deleted_user"
    url = "https://www.reddit.com/r/singapore/comments/8cs8b0/marsiling_at_sunrise/dxk89g2/"
    expected_post = (
        "Marsiling-er here too. North side best side! go JB shop till u drop"
    )
    expected_credit = (
        f'2018 Apr 18, Deleted User. r/singapore, "Marsiling at Sunrise". {url}'
    )

    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )


def test_list_in_reply() -> None:
    test_suffix_for_caching = "list"
    url = "https://www.reddit.com/r/askSingapore/comments/sd00v4/what_is_an_unsolved_mystery_in_singapore/hua69nt/"
    expected_post = "- Why do we need a mayor?<br>- Was Bukit Ho Swee Fire an inside job so that we can have HDB?<br>- Is tekong cough a placebo effect or is there something in the water?<br>- Why MRT actually comes faster than what's displayed on the next arriving timing?<br>- Did Sang nila utama see a lion?<br>/s"  # noqa: E501
    expected_credit = (
        "2022 Jan 26, u/BakeMate. r/askSingapore, "
        f'"What is an unsolved mystery in Singapore?". {url}'
    )

    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )


def test_able_to_get_past_18_plus_check() -> None:
    test_suffix_for_caching = "18_plus_check"
    url = "https://www.reddit.com/r/askSingapore/comments/1icl0q9/is_it_normal_for_ur_dad_to_strip_naked_in_front/m9uo106/"
    expected_post = "I guess this is called gong xi fuck cai"
    expected_credit = (
        "2025 Jan 29, u/DurianNational6775. r/askSingapore, "
        '"Is it normal for ur dad to strip naked in front of u? Even in SG families". '  # noqa: E501
        f"{url}"
    )

    url_checker.assert_produces_post_and_credit(
        url=url,
        test_suffix_for_caching=test_suffix_for_caching,
        expected_post=expected_post,
        expected_credit=expected_credit,
    )
