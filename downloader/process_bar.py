_FMT = '[{done_str}{empty_str}]{done_num}%'


def make_process_bar(total, init_has_load=0):
    """ 构建process_bar, 显示进度条
    argv:
        total：文件总字节数
        init_has_load：已下载字节数
    use:
        process_bar = make_process_bar(total, init_has_load=0)
        process_bar(has_load)
    """
    done_num = int(init_has_load / total * 100)
    print(
        _FMT.format(
            done_str=">".rjust(done_num, '#'),
            empty_str=" " * (100 - done_num),
            done_num=done_num
        ),
        end='\r'
    )

    def process_bar(has_load):
        """ 传入has_load，显示进度 """
        nonlocal done_num
        new_done_num = int(has_load / total * 100)
        if done_num != new_done_num:
            done_num = new_done_num
            # rest_num = 100 - done_num
            print(
                _FMT.format(
                    done_str=">".rjust(done_num, '#'),
                    empty_str=" " * (100 - done_num),
                    done_num=done_num
                ),
                end='\r'
            )
        if done_num == 100:
            print()

    return process_bar

