from res_manager import ResultManager


def test_all():
    rm = ResultManager('.')
    rm.save([1, 2, 3], topic='test saving', name='data1', comment='Test saving a list')
    rm.save(65535, topic='test saving', comment='Test saving a number without a name')
    rm.save(rm, topic='topic 2', name="object of \"ResultManager\"", comment='Saving an object')
    rm.save({0: 1, 1: 'string'}, name="hongshan's dict without topic")
    rm.print_meta_info()
    rm.load(3)
    rm.load(3, version='first')
    rm.delete_by_id(3, version='latest')
    rm.update_meta(1, name='b', topic='topic 5')
