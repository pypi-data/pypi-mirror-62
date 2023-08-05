# -*- coding: utf-8 -*-
import logging
from time import sleep
from automatontools.finders import find_element, find_from_elements, find_sub_element_from_element
from automatontools.information import is_field_exist, is_field_displayed
from automatontools.drivers_tools import web_drivers_tuple
from selenium.common.exceptions import InvalidElementStateException, NoSuchElementException, \
    StaleElementReferenceException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

log = logging.getLogger(__name__)


def __field_validation(field=None):
    """
    Check if the field contains the expected keys and values for the type key.
    :param field: a dictionary
    :return: True if field is correct false otherwise
    """
    response = False
    if isinstance(field, dict) \
            and all([key in field.keys() for key in ("type", "value")]) \
            and field['type'] in ["id", "name", "class_name", "link_text", "css",
                                  "partial_link_text", "xpath", "tag_name"]:
        response = True
    return response


def fill_elements(driver=None, fields=None, data=None):
    """
    Fill a field set with data where the field and data are identified by the same key
    Keys are taken from the data set dictionary
    :param driver: a selenium web driver
    :param fields: a dictionary
    :param data: a dictionary
    :raise AssertionError: driver is not define, fields and data doesn't have the same keys
    :raise InvalidElementStateException: rethrown from fill_element
    :raise Exception: all other issues
    :return: 0 if success
    """
    try:
        assert driver is not None and isinstance(driver, web_drivers_tuple()),\
            "Driver is expected."
        assert all(key in fields.keys() for key in
                   data.keys()), \
            "Missing fields for the given data. Data keys '{}'. Fields keys '{}'".format(
                data.keys(),
                fields.keys())  # Check that the fields dictionary contains enough keys

        for key in data:
            fill_element(driver=driver, field=fields[key], value=data[key])

        return 0
    except AssertionError as assertion:
        log.error("automatontools.actions.fill_elements raised an assertion with following"
                  " input driver:'{}', fields:'{}' and data:'{}'."
                  " Assertion is '{}'".format(driver, fields, data, assertion.args))
        raise
    except InvalidElementStateException:
        raise
    except Exception as exception:
        logging.error(exception.args)
        raise Exception(exception.args[0]) from None


def fill_element(driver=None, field=None, value=None):
    """
    Fill the given field with the value.
    :param driver: a selenium web driver
    :param field: a dictionary
    :param value: a string or castable to string
    :raise AssertionError: driver is not define, field fails validation
    :raise InvalidElementStateException: if the element is not user-editable
    :raise Exception: web element not found
    :return: 0 if success
    """
    try:
        assert driver is not None and isinstance(driver, web_drivers_tuple()),\
            "Driver is expected."
        assert __field_validation(field=field), "Field '{}' is not a valid field".format(field)

        elem = find_element(driver=driver, field=field)
        if value:
            elem.clear()
            elem.send_keys(str(value))
        else:
            number_of_backspace_hit = len(elem.get_attribute('value'))
            elem.send_keys(number_of_backspace_hit * Keys.BACKSPACE)
        return 0
    except AssertionError as assertion:
        log.error("automatontools.actions.fill_element raised an assertion with following"
                  " input driver:'{}', field:'{}' and value:'{}'."
                  " Assertion is '{}'".format(driver, field, value, assertion.args))
        raise
    except InvalidElementStateException as invalid_element:
        log.error(invalid_element)
        invalid_element.args = ("Element '{}' must be user-editable".format(field),)
        raise InvalidElementStateException(
            "Element '{}' must be user-editable".format(field)) from None
    except Exception as exception:
        logging.error(
            "automatontools.actions.fill_element raised an exception. Exception is '{}'".format(
                exception.args))
        raise Exception(
            "automatontools.actions.fill_element raised an exception. Exception is '{}'".format(
                exception.args[0])) from None


def select_in_dropdown(driver=None, field=None, visible_text=None, value=None):
    """
    see https://stackoverflow.com/questions/7867537/selenium-python-drop-down-menu-option-value
    see https://sqa.stackexchange.com/questions/1355/what-is-the-correct-way-to-select-an-option-using-seleniums-python-webdriver # noqa
    see https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.select.html # noqa
    :raise AssertionError: driver is not define, field is not valid
    :return:
    """
    assert driver is not None and isinstance(driver, web_drivers_tuple()), "Driver is expected."
    assert __field_validation(field), "Field '{}' is not a valid field".format(field)

    try:
        my_select = Select(find_element(driver=driver, field=field))

        if visible_text is not None:
            my_select.select_by_visible_text(visible_text)
        elif value is not None:
            my_select.select_by_value(value)
        else:
            raise Exception("select_in_dropdown can't select with no value.")

        return 0

    except NoSuchElementException as no_such_element:
        log.error(no_such_element.args)
        raise NoSuchElementException(no_such_element.args[0]) from None
    except Exception as exception:
        log.error(exception.args)
        raise Exception(exception.args[0]) from None


def select_in_angular_dropdown(driver=None, root_field=None, visible_text: str = None):
    """
    Select a field within a mat_option list

    If root_field is defined then click it and search for visible_text in mat-option elements.
    Otherwise only search for visible_text in mat-options elements
    :param visible_text: a string to search
    :param driver: a selenium web driver
    :param root_field: a dictionary for the container
    :return:
    """
    try:
        if root_field is not None:
            click_element(driver=driver, field=root_field)
            sleep(0.1)

        if is_field_exist(driver=driver, field={"type": "tag_name", "value": "mat-option"}):
            element = find_from_elements(driver=driver,
                                         field={"type": "tag_name", "value": "mat-option"},
                                         text=visible_text)
            element.click()
        else:
            raise Exception('No options displayed within 5 seconds')

    except StaleElementReferenceException as stale_exception:
        log.warning("StaleElementReferenceException. Selection should be done.\n{}".format(
            stale_exception.args))
        return 0
    except Exception as exception:
        log.error(exception.args)
        raise Exception(exception.args[0]) from None


def click_element(driver=None, field=None, inner_element_to_click=None):
    """
    Do simple left click on the given field or on the sub element designed by inner_element_to_click
    :param driver: a selenium web driver
    :param field: a dictionary
    :param inner_element_to_click: a dictionary as field element
    :raise AssertionError: driver is not define, field is not valid
    :return: 0 if success
    """
    assert driver is not None and isinstance(driver, web_drivers_tuple()), "Driver is expected."
    assert __field_validation(field), "Field '{}' is not a valid field".format(field)
    assert inner_element_to_click is None or __field_validation(inner_element_to_click),\
        "Field '{}' is not a valid field".format(field)
    try:
        web_element = find_element(driver=driver, field=field)
        if inner_element_to_click is None:
            web_element.click()
        else:
            sub_web_element = find_sub_element_from_element(web_element=web_element,
                                                            field=inner_element_to_click)
            sub_web_element.click()
        return 0
    except Exception as exception:
        logging.error(exception.args)
        raise Exception(exception.args[0]) from None


def set_checkbox(driver=None, field=None, is_checked=None):
    """
    Set a checkbox to a specific state: True for checked, False for unchecked
    :param driver: a selenium web driver
    :param field: a field identifier as a dictionary
    :param is_checked: the field check value as a boolean (True/False)
    :raise AssertionError: driver is not define, field is not valid, is_checked is not a boolean
    :return: 0 if success
    """
    assert driver is not None and isinstance(driver, web_drivers_tuple()), "Driver is expected."
    assert __field_validation(field), "Field '{}' is not a valid field".format(field)
    assert isinstance(is_checked, bool), "is_checked is expected to be a boolean."

    try:
        elem = find_element(driver=driver, field=field)
        current_state = bool(elem.get_attribute("checked"))
        if current_state is not is_checked:
            elem.click()

        # Check if the element has been set in the expected status
        current_state = bool(elem.get_attribute("checked"))
        if current_state is not is_checked:
            raise Exception(
                "The element '{}' can't be set to the expected status '{}'.".format(field,
                                                                                    is_checked))
        return 0

    except Exception as exception:
        logging.error(exception.args)
        raise Exception(exception.args[0]) from None


def hover_element(driver=None, field=None):
    """
    Do simple hover on the given field
    :param driver: a selenium web driver
    :param field: a dictionary
    :raise AssertionError: driver is not define, field is not valid
    :return: 0 if success
    """
    assert driver is not None and isinstance(driver, web_drivers_tuple()), "Driver is expected."
    assert __field_validation(field), "Field '{}' is not a valid field".format(field)
    try:
        elem = find_element(driver=driver, field=field)
        hover = ActionChains(driver).move_to_element(elem)
        hover.perform()
        return 0
    except Exception as exception:
        logging.error(exception.args)
        raise Exception(exception.args[0]) from None


def select_in_elements(driver=None, field=None, displayed_text=None):
    """
    Do a click on the element which text
    :param driver: a selenium web driver
    :param field: a dictionary
    :param displayed_text: a string
    :return: 0 if success
    """

    assert driver is not None and isinstance(driver, web_drivers_tuple()), "Driver is expected."
    assert __field_validation(field), "Field '{}' is not a valid field".format(field)
    assert displayed_text is not None and isinstance(displayed_text, str), \
        "Displayed text must be a non-empty string"
    try:
        if is_field_displayed(driver=driver, field=field):
            element = find_from_elements(driver=driver, field=field, text=displayed_text)
            element.click()
        return 0
    except Exception as exception:
        logging.error(exception.args)
        raise Exception(exception.args[0]) from None
