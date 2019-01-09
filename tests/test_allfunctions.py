from res_manager import ResultManager
import os


def test_all():
    if os.path.exists('./data.db'):
        os.remove('./data.db')
    rm = ResultManager('.')
    rm.save([1, 2, 3], topic='test saving', name='data1', comment='Test saving a list')
    rm.save(65535, topic='test saving', comment='Test saving a number without a name')
    rm.save(rm, topic='topic 2', name="object of \"ResultManager\"", comment='Saving an object')
    rm.save({0: 1, 1: 'string'}, name="hongshan's dict without topic")
    rm.print_meta_info()
    rm.load(3)
    rm.load(3, version='first')
    rm.delete_by_id(3, version='latest')
    rm.update_meta(2, name='name', topic='topic 5')
    rm.save(12, name='b', topic='topic 5')
    rm.save(12, name='b', topic='topic 5')
    rm.save(14, name='b', topic='topic 5', replace_version='latest')
    rm.save(14, name='name', topic='topic 5', replace_version='latest')
    rm.save(13, name='b', topic='topic 5')
    rm.print_meta_info()
    print(rm.load(5, version='first'))
    print(rm.load(5))
    rm.print_meta_info(topic='topic 5')
    return rm


if __name__ == '__main__':
    rm = test_all()
