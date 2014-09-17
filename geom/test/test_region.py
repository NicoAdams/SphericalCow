import pytest
import sys, os, imp
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

region = imp.load_source('region', 'geom/region.py')
from region import Region

r0 = Region(0,0)
r1 = Region(0,10)
r2 = Region(10,0)

r3 = Region(-3,1)
r4 = Region(1,3)
r5 = Region(9,11)
r6 = Region(-3,13)
r7 = Region(-90, 101)

def test_init():
	assert r0.left == 0 and r0.right == 0
	assert r1.left == 0 and r1.right == 10
	assert r2.left == 0 and r2.right == 10
	
def test_len():
	assert r0.len() == 0
	assert r1.len() == 10
	assert r2.len() == 10
	assert r3.len() == 4
	assert r4.len() == 2
	assert r5.len() == 2
	assert r6.len() == 16
	
def test_center():
	assert r0.center() == 0
	assert r1.center() == 5
	assert r2.center() == 5
	assert r3.center() == -1
	assert r4.center() == 2
	assert r5.center() == 10
	assert r6.center() == 5

def test_overlaps():
	assert not r0.overlaps(r0)
	assert not r0.overlaps(r1)
	assert not r1.overlaps(r0)
	assert r1.overlaps(r2)
	assert r2.overlaps(r1)
	assert r1.overlaps(r3)
	assert r1.overlaps(r4)
	assert r1.overlaps(r5)
	assert r1.overlaps(r6)
	assert not r3.overlaps(r4)
	assert not r3.overlaps(r5)

def test_overlapRegion():
	assert r0.overlapRegion(r0) == False
	assert r0.overlapRegion(r1) == False
	assert r1.overlapRegion(r0) == False
	assert r1.overlapRegion(r2) == Region(0,10)
	assert r2.overlapRegion(r1) == Region(0,10)
	assert r1.overlapRegion(r3) == Region(0,1)
	assert r1.overlapRegion(r4) == Region(1,3)
	assert r1.overlapRegion(r5) == Region(9,10)
	assert r1.overlapRegion(r6) == Region(0,10)
	assert r3.overlapRegion(r4) == False
	assert r3.overlapRegion(r5) == False
	
def test_minTranslation():
	assert r0.minTranslation(r0) == 0
	assert r0.minTranslation(r1) == 0
	assert r1.minTranslation(r0) == 0
	assert r1.minTranslation(r2) == 10
	assert r2.minTranslation(r1) == 10
	assert r1.minTranslation(r3) == -1
	assert r1.minTranslation(r4) == -3
	assert r1.minTranslation(r5) == 1
	assert r1.minTranslation(r6) == 13
	assert r3.minTranslation(r4) == 0
	assert r3.minTranslation(r5) == 0
	assert r1.minTranslation(r7) == 100
	