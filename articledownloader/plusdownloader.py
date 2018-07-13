import requests
from bs4 import BeautifulSoup 
from requests.utils import quote
import re
import json
import scrapers
from autologging import logged, traced
from csv import reader
from time import sleep

@logged
class PlusDownloader:

  def __init__(self, sleep_sec=1, timeout_sec=30):
    '''
    Initialize and set up API keys
    :param els_api_key: API key for Elsevier (for Elsevier's API)
    :type els_api_key: str
    :param sleep_sec: Sleep time between API calls (default = 1s)
    :type sleep_sec: int
    :param timeout_sec: Max time before timeout (default = 30s)
    :type timeout_sec: int
    '''
    self.sleep_sec = sleep_sec
    self.timeout_sec = timeout_sec

  @traced
  def get_html_from_doi(self, doi, writefile, mode):
    
    if mode == 'aps':
        base_url='https://journals.aps.org/prl/abstract/'
        url=base_url + doi + '#fulltext'
        r = requests.get(url, stream=True, timeout=self.timeout_sec)
        if r.status_code == 200:
            for chunk in r.iter_content(2048):
                writefile.write(chunk)
        return True
    
    if mode == 'aip':
        base_url='https://aip.scitation.org/doi/'
        url=base_url + doi
        r = requests.get(url, stream=True, timeout=self.timeout_sec)
        if r.status_code == 200:
            for chunk in r.iter_content(2048):
                writefile.write(chunk)
        return True

    if mode == 'pnas':
        base_url='http://dx.doi.org/'
        url=base_url + doi
        r = requests.get(pdf_url, stream=True, timeout=self.timeout_sec)
        if r.status_code == 200:
            for chunk in r.iter_content(2048):
                writefile.write(chunk)
        return True
    
  @traced
  def get_pdf_from_doi(self, doi, writefile, mode):
    '''
    Downloads and writes a PDF article to a file, given a DOI and operating mode
    :param doi: DOI string for the article we want to download
    :type doi: str
    :param writefile: file object to write to
    :type writefile: file
    :param mode: either 'crossref' | 'elsevier' | 'rsc' | 'springer' | 'ecs' | 'nature' | 'acs', depending on how we wish to access the file
    :type mode: str
    :returns: True on successful write, False otherwise
    :rtype: bool
    '''

    if mode == 'aip':
        base_url='https://aip.scitation.org/doi/pdf/'
        pdf_url=base_url + doi
        r = requests.get(pdf_url, stream=True, timeout=self.timeout_sec)
        if r.status_code == 200:
            for chunk in r.iter_content(2048):
                writefile.write(chunk)
        return True
    
    if mode == 'science':
        base_url='http://science.sciencemag.org/content/'
        back='.pdf'
        pdf_url=base_url + doi #+ back
        
        headers = {
            'Accept': 'application/pdf'
        }
        r = requests.get(pdf_url, stream=True, headers=headers, timeout=self.timeout_sec)
        if r.status_code == 200:
            for chunk in r.iter_content(2048):
                writefile.write(chunk)
        return True

  @traced
  def get_abstract_from_doi(self, doi, mode):
    '''
    Returns abstract as a unicode string given a DOI
    :param doi: DOI string for the article we want to grab metadata for
    :type doi: str
    :param mode: Only supports 'elsevier' for now
    :type mode: str
    :returns: An abstract (or None on failure)
    :rtype: unicode
    '''
    
    if mode == 'acs':
        try:
            url='http://pubs.acs.org/doi/abs/' + doi
            
            headers = {
                'User-agent': 'Mozilla/5.0'
            }
            r = requests.get(url, stream=True, headers=headers, timeout=self.timeout_sec)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "lxml")
                tag = soup.find(class_="articleBody_abstractText")
                return tag.text
        except:
            return None
            
        return None