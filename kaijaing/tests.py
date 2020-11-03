def order_track(request):   #查找状态是画图完成或者是拉图完成的明细
    post_data = request.body
    post_data = json.loads(post_data)
    user_json = []
    user_data = {}
    selectForm = post_data.get('serch')
    if selectForm.get('id') or selectForm.get('draw_time') or selectForm.get('print_time') or selectForm.get('order_code') or selectForm.get('draw_status') or selectForm.get(
            'order_level') or selectForm.get('color') or selectForm.get('words') or selectForm.get('print_status')  or selectForm.get('item_name')\
            or selectForm.get('type') or selectForm.get('order_name') or selectForm.get('salesman') or selectForm.get('order_status') or selectForm.get('order_status'):
        user_list = Order_Del.objects.all()
        if selectForm.get('draw_time'): #画图时间
            draw_time = selectForm.get('draw_time')
            begin_draw = draw_time[0][:10] + ' 00:00'
            end_draw = draw_time[1][:10] + ' 24:00'
            user_list = user_list.filter(draw_time__gte=begin_draw, draw_time__lte=end_draw)
        if selectForm.get('print_time'): #画图时间
            draw_time = selectForm.get('print_time')
            begin_draw = draw_time[0][:10] + ' 00:00'
            end_draw = draw_time[1][:10] + ' 24:00'
            user_list = user_list.filter(print_time__gte=begin_draw, print_time__lte=end_draw)
        if selectForm.get('order_code'):
            order_code = selectForm.get('order_code')
            order_code = order_code.replace('，',',') #替换逗号
            order_code_li = order_code.split(',')  #生成列表
            if len(order_code_li) == 1:#长度为1时
                user_list = user_list.filter(order_code__contains=selectForm.get('order_code'))
            else:
                user_list = user_list.filter(order_code__in=order_code_li)
        if selectForm.get('id'):
            id = selectForm.get('id')
            id = id.replace('，',',') #替换逗号
            id_li = id.split(',')  #生成列表
            #转化为整数
            id_li=list(map(int, id_li))
            user_list = user_list.filter(id__in=id_li)
        if selectForm.get('draw_status'):
            user_list = user_list.filter(draw_status=selectForm.get('draw_status'))
        if selectForm.get('order_level'):
            user_list = user_list.filter(order_level=selectForm.get('order_level'))
        if selectForm.get('color'):
            user_list = user_list.filter(color=selectForm.get('color'))
        if selectForm.get('words'):
            user_list = user_list.filter(words=selectForm.get('words'))
        if selectForm.get('type'):
            user_list = user_list.filter(skutype=selectForm.get('type'))
        if selectForm.get('order_name'):
            user_list = user_list.filter(order_name__icontains=selectForm.get('order_name'))
        if selectForm.get('salesman'):
            user_list = user_list.filter(salesman__contains=selectForm.get('salesman'))
        if selectForm.get('print_status'):
            user_list = user_list.filter(print_status__contains=selectForm.get('print_status'))
        if selectForm.get('item_name'):
            user_list = user_list.filter(item_name__icontains=selectForm.get('item_name'))
        if selectForm.get('order_status'):
            order_status = selectForm.get('order_status')
            user_list = user_list.filter(Q(state=order_status) | Q(refund=order_status) | Q(Rework=order_status))
        user_list = user_list.values().order_by('-id')  # 转换取值

    else:
        user_list = Order_Del.objects.all().values().order_by('-id')
    total = Paginator(user_list, post_data.get('size')).count  # 总计的数量
    if total <post_data.get('size') * post_data.get('page'):
        user_page = Paginator(user_list, post_data.get('size')).page(1)
    else:
        user_page = Paginator(user_list, post_data.get('size')).page(post_data.get('page'))
    user_data['user_list'] = list(user_page)
    user_data['total'] = total
    return JsonResponse(data=user_data, safe=False))