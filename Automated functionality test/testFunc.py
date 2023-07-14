import unittest
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import time



class VerifyFunctionailty(unittest.TestCase):


    @classmethod
    def setUpClass(inst):
        inst.browser = webdriver.Chrome('./chromedriver')
        inst.browser.title
        inst.browser.maximize_window()
        inst.target = 'http://dm571.herokuapp.com/' # http://dm571.herokuapp.com/ or localhost:8000
        inst.browser.get(inst.target)

    def test_A_accessOnlineVagtplan(self):
        self.browser.get(self.target)
        self.assertEqual('Log In', self.browser.title)
        time.sleep(1)
    
    def test_B_restrictAccess(self):
        self.browser.get(self.target + 'event/new/')
        self.assertNotEqual('New Event',self.browser.title)
        time.sleep(1)

    def test_C_loginService(self):
        self.browser.get(self.target + 'accounts/login/?next=/')
        username = 'unittest'
        password = 'selenium'
        usernameField = self.browser.find_element_by_name('username')
        passwordField = self.browser.find_element_by_name('password')
        usernameField.send_keys(username)
        passwordField.send_keys(password)
        login = self.browser.find_element_by_css_selector('[type="submit"]')
        login.click()
        time.sleep(1)

    def test_D_calendarLastNext(self):
        lastWeek = self.browser.find_element_by_class_name('fa-chevron-left.mr-1')
        lastWeek.click()
        time.sleep(1)
        nextWeek = self.browser.find_element_by_class_name('fa-chevron-right.ml-1')
        nextWeek.click()
        time.sleep(1)

    def test_E_createNewEvent(self):
        createEvent = self.browser.find_element_by_css_selector('[href="/event/new/"]')
        createEvent.click()
        title = self.browser.find_element_by_name('title')
        title.send_keys('Test event created by unittest')
        description = self.browser.find_element_by_name('description')
        description.send_keys('This event was created by the unittest')
        next = self.browser.find_element_by_css_selector('[type="submit"]')
        next.click()

    def test_F_addShifts(self):
        shift = Select(self.browser.find_element_by_name('shift_type'))
        shift.select_by_visible_text('Cleaning')
        description = self.browser.find_elements_by_xpath('//textarea[@name="description"]')
        description[1].send_keys('A test shift created to the test event')
        start = self.browser.find_element_by_name('start')
        start.click()
        start.clear()
        startTime = (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d %H:%M:%S")
        start.send_keys(startTime)
        end = self.browser.find_element_by_name('end')
        end.click()
        end.clear()
        endTime = (datetime.now() + timedelta(days=1, hours=3)).strftime("%Y-%m-%d %H:%M:%S")
        end.send_keys(endTime)
        add = self.browser.find_element_by_xpath('//*[contains(text(), "Add shift")]')
        add.click()
        next = self.browser.find_element_by_xpath('//*[contains(text(), "Done")]')
        next.click()
        exists = False
        time.sleep(1)

    def test_G_inspectAndSignUp(self):
        self.browser.find_element_by_partial_link_text('OnlineVagtplan').click()
        event = self.browser.find_element_by_partial_link_text('Test event')
        event.click()
        time.sleep(1)
        signUp = self.browser.find_element_by_xpath('//*[contains(text(), "Cleaning")]')
        signUp.click()
        time.sleep(1)
        next = self.browser.find_element_by_xpath('//*[contains(text(), "Yes, Take Shift")]')
        next.click()
        time.sleep(1)

    def test_H_deleteEvent(self):
        event = self.browser.find_element_by_partial_link_text('Test event')
        event.click()
        manage = self.browser.find_element_by_xpath('//*[contains(text(), "Manage Event")]')
        manage.click()
        delete = self.browser.find_element_by_class_name('btn.btn-outline-danger')
        delete.click()
        time.sleep(1)
        next = self.browser.find_element_by_xpath('//*[contains(text(), "Yes, Delete Event")]')
        next.click()
        time.sleep(1)

        

    def test_I_accessGroupsAndUsers(self):
        self.browser.find_element_by_partial_link_text('OnlineVagtplan').click()
        groupsAndUsers = self.browser.find_element_by_link_text('Groups and Users')
        groupsAndUsers.click()
        time.sleep(1)

    def test_J_createNewGroup(self):
        createGroup = self.browser.find_element_by_xpath('//*[contains(text(), "Create New Group")]')
        createGroup.click()
        title = self.browser.find_element_by_name('title')
        title.send_keys('Unittest Group')
        groupType = Select(self.browser.find_element_by_name('group_type'))
        groupType.select_by_visible_text('Other')
        description = self.browser.find_element_by_name('description')
        description.send_keys('This group was created by the unittest')
        next = self.browser.find_element_by_css_selector('[type="submit"]')
        next.click()
        time.sleep(1)

    def test_K_addToGroup(self):
        groupsAndUsers = self.browser.find_element_by_link_text('Groups and Users')
        groupsAndUsers.click()
        group = self.browser.find_element_by_partial_link_text('Unittest Group')
        group.click()
        addToGroup = self.browser.find_element_by_xpath('//*[contains(text(), "Add Members to Group")]')
        addToGroup.click()
        userCheck = self.browser.find_element_by_xpath('//input[@type="checkbox"][@name="selected_user"][@value="8"]')
        userCheck.click()
        next = self.browser.find_element_by_xpath('//*[contains(text(), "Add Selected Users to Group")]')
        next.click()
        time.sleep(1)


    def test_L_removeFromGroup(self):
        groupsAndUsers = self.browser.find_element_by_link_text('Groups and Users')
        groupsAndUsers.click()
        group = self.browser.find_element_by_partial_link_text('Unittest Group')
        group.click()
        remove = self.browser.find_element_by_class_name("fa-user-minus.text-dark.p")
        remove.click()
        time.sleep(1)
        confirm = self.browser.find_element_by_xpath('//*[contains(text(), "Yes, Remove Member")]')
        confirm.click()
        time.sleep(1)


    def test_M_deleteGroup(self):
        delete = self.browser.find_element_by_class_name('btn.btn-outline-danger')
        delete.click()
        time.sleep(1)
        confirm = self.browser.find_element_by_xpath('//button[@class="btn btn-danger"][contains(text(), "Yes, Delete Group")]')
        confirm.click()
        time.sleep(1)

    def test_Z_logout(self):
        menu = self.browser.find_element_by_id('userMenu')
        menu.click()
        time.sleep(1)
        logout = self.browser.find_element_by_css_selector('[href="/accounts/logout/"]')
        logout.click()
        time.sleep(1)

    @classmethod
    def tearDownClass(inst):
        time.sleep(3)
        inst.browser.quit()

if __name__ == "__main__":
    unittest.main()
