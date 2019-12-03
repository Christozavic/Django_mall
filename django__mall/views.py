from _datetime import datetime
import logging
from django.shortcuts import render

from accounts.models import User
from mall.models import Product
from system.models import Slider, News
from utils import constants

logger = logging.getLogger(__name__)

def index(request):
    """ 首页 """
    # 记录调试信息
    logger.debug('调试信息debug')
    logger.info('普通信息info')
    logger.error('异常error')
    print('request.my_user: ', request.my_user)
    # 查询轮播图
    slider_list = Slider.objects.filter(types=constants.SLIDER_TYPE_INDEX)

    # 首页的新闻
    now_time = datetime.now()
    # 置顶的，有效的，在时间范围内的
    news_list = News.objects.filter(types=constants.NEWS_TYPE_NEW,
                                    is_top=True,
                                    is_valid=True,
                                    start_time__lte=now_time,
                                    end_time__gte=now_time)
    # 游戏推荐
    yx_list = Product.objects.filter(status=constants.PRODUCT_STATUS_SELL, is_valid=True, tags__code='yxtj')
    # 精选
    jx_list = Product.objects.filter(status=constants.PRODUCT_STATUS_SELL, is_valid=True, tags__code='jx')
    # # 从session中获取用户ID
    # user_id = request.session[constants.LOGIN_SESSION_ID]
    # print(user_id)
    # # 查询当前登录的用户
    # user = User.objects.get(pk=user_id)
    return render(request, 'index.html', {
        'slider_list': slider_list,
        'news_list': news_list,
        'yx_list': yx_list,
        'jx_list': jx_list,
        # 'user_id': user_id,
    })
