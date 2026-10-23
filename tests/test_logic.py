"""Offline logic checks using a tiny fake browser DOM. No network required."""
from __future__ import annotations
import importlib.util
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from datetime import date, timedelta
import unittest

SITE=Path(__file__).resolve().parents[1]

class ClassList:
    def __init__(self): self.names=set()
    def add(self, name): self.names.add(name)
    def remove(self, name): self.names.discard(name)

class Element:
    def __init__(self, value='', checked=False, dataset=None):
        self.value=value;self.checked=checked;self.dataset=SimpleNamespace(**(dataset or {}))
        self.hidden=False;self.textContent='';self.href='';self.classList=ClassList();self.children=[]
        self.attributes={};self.files=SimpleNamespace(length=0,item=lambda index: None)
    def replaceChildren(self): self.children=[]
    def appendChild(self,child): self.children.append(child)
    def setAttribute(self,k,v): self.attributes[k]=v
    def scrollIntoView(self): self.scrolled=True
    def checkValidity(self): return True
    def reportValidity(self): return True

class FakeDocument:
    def __init__(self,defaults=None):
        self.nodes={k:Element(v) for k,v in (defaults or {}).items()};self.groups={}
    def querySelector(self,k): return self.nodes.setdefault(k,Element())
    def querySelectorAll(self,k): return self.groups.get(k,[])
    def createElement(self,k): return Element()

def load_module(script, defaults):
    doc=FakeDocument(defaults)
    lib=ModuleType('pyscript')
    lib.document=doc
    lib.window=SimpleNamespace(print=lambda:None)
    lib.when=lambda *args,**kwargs: lambda function:function
    sys.modules['pyscript']=lib
    spec=importlib.util.spec_from_file_location('temp_'+script, SITE/'scripts'/script)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
    return obj,doc

class BytePrintTests(unittest.TestCase):
    def test_services_color_and_pickup(self):
        app,doc=load_module('services.py', {'#service-type':'color','#service-quantity':'4','#service-copies':'2'})
        doc.querySelector('#service-pickup').checked=True
        app.update_quote()
        self.assertEqual(doc.querySelector('#service-total').textContent,'₱83.00')
    def test_services_rental_and_invalid(self):
        app,doc=load_module('services.py', {'#service-type':'rental','#service-quantity':'2','#service-copies':'1'})
        self.assertEqual(doc.querySelector('#service-total').textContent,'₱40.00')
        doc.querySelector('#service-quantity').value='-3';app.update_quote()
        self.assertEqual(doc.querySelector('#service-total').textContent,'—')
    def test_pickup_estimate_and_draft(self):
        app,doc=load_module('pickup.py', {'#pickup-type':'bw','#pickup-pages':'5','#pickup-copies':'1','#pickup-date':(date.today()+timedelta(days=3)).isoformat(), '#customer-name':'Alex Santos','#customer-email':'alex@example.com','#pickup-time':'13:00','#pickup-paper':'A4','#pickup-payment':'Cash at pickup'})
        self.assertEqual(doc.querySelector('#pickup-total').textContent,'₱27.50')
        app.create_draft(SimpleNamespace(preventDefault=lambda:None))
        text=doc.querySelector('#request-summary').textContent
        self.assertIn('Alex Santos',text)
        self.assertIn('NOT SUBMITTED',text)
        self.assertTrue(doc.querySelector('#request-result').scrolled)
    def test_pickup_rejects_old_date(self):
        app,doc=load_module('pickup.py', {'#pickup-type':'bw','#pickup-pages':'5','#pickup-copies':'1','#pickup-date':'2020-01-01'})
        app.create_draft(SimpleNamespace(preventDefault=lambda:None))
        self.assertIn('future pickup date',doc.querySelector('#pickup-error').textContent)
    def test_shop_basket_filter_and_clear(self):
        app,doc=load_module('shop.py', {'#product-search':''})
        cards=[Element(dataset={'category':'supplies','name':'ballpen'}),Element(dataset={'category':'snacks','name':'biscuit'})]
        doc.groups['.product-card']=cards
        app.active_category='snacks';app.update_visible_products()
        self.assertTrue(cards[0].hidden);self.assertFalse(cards[1].hidden)
        app.add_to_basket(SimpleNamespace(currentTarget=Element(dataset={'name':'Ballpen','price':'12'})))
        app.add_to_basket(SimpleNamespace(currentTarget=Element(dataset={'name':'Ballpen','price':'12'})))
        self.assertEqual(doc.querySelector('#basket-total').textContent,'₱24.00')
        app.clear_basket(None)
        self.assertEqual(doc.querySelector('#basket-total').textContent,'₱0.00')
    def test_home_click_recommendation(self):
        app,doc=load_module('home.py', {})
        button=Element(dataset={'need':'computer'})
        doc.groups['.choice']=[button]
        app.recommend_service(SimpleNamespace(currentTarget=button))
        self.assertEqual(doc.querySelector('#recommend-title').textContent,'Find computer access')
        self.assertEqual(doc.querySelector('#recommend-link').href,'services.html')

if __name__=='__main__':unittest.main()
