# Copyright (c) 2012, the Dart project authors.  Please see the AUTHORS file
# for details. All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.

from models.package import Package
from testcase import TestCase

class PackageUploadersTest(TestCase):
    def setUp(self):
        super(PackageUploadersTest, self).setUp()
        self.package = Package.new(
            name='test-package',
            uploaders=[self.normal_user('uploader1'),
                       self.normal_user('uploader2')])
        self.package.put()

    def test_uploader_creates_new_uploader(self):
        self.be_normal_oauth_user('uploader1')
        response = self.testapp.post('/packages/test-package/uploaders.json',
                                     {'email': self.normal_user().email()})
        self.assert_json_success(response)

        package = Package.get_by_key_name('test-package')
        self.assertEquals(package.uploaders, [
            self.normal_user('uploader1'),
            self.normal_user('uploader2'),
            self.normal_user()
        ])

    def test_uploader_deletes_uploader(self):
        self.be_normal_oauth_user('uploader1')
        response = self.testapp.delete(
            '/packages/test-package/uploaders/%s.json' %
                self.normal_user('uploader1').email())
        self.assert_json_success(response)

        package = Package.get_by_key_name('test-package')
        self.assertEquals(
            package.uploaders, [self.normal_user('uploader2')])
