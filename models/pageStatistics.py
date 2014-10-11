#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A Simple Page Statistics Plugin

Filename:   pageStatistics.py
Author:     Anton G. Mueckl
Contact:    amueckl@chartup.de

Date:       2009-11-13
Version:    1.0
Licence:    GPL v2

Inspired by:
Hierarchical Category Tree by Thadeus Burgess, see:
http://www.web2pyslices.com/main/slices/take_slice/27

Usage:
Create a new file models/pageStatistics.py and copy this slice into it.
If you want to get the results displayed to the visitor, also add to
views/layout.html:

<p>
    <center>
        <font size="1">Hits: <u>{{=pageStatistics.hits}}</u> Visits: <u>{{=pageStatistics.visits}}</u></font>
    </center>
</p>

If you want to set other starting values than 0, you also can define one like:
pageStatistics = PageStatistics(db, initialHits=16548, initialVisits=6541)() # see below:

"""

class PageStatistics():
    title = "PageStatistics"
    keywords = "hit counter, page statistics, visits"
    description = "Defines database models and functions for page stats"
    copyright = "GPL v2"

    def __init__(self,
                 db,                                # reference to DAL obj.
                 initialVisits=0,                   # visits intial value 
                 tablename="visitas"                # you may want to alter
                                                    # the name of the
                                                    # database table
                 ):
        self._db = db
        self._tablename = tablename
        self._initialVisits = initialVisits

    def __call__(self):
        self.define_tables()
        self.populate()
        self.update()
        return self

    def define_tables(self):
        self._table = self._db.define_table(self._tablename,
            Field('visits', 'integer'),
        )

        self.table = self._table
        self.fieldVisits = "%s.visits" % self._table
        pass

    def populate(self):
        # populate if neccessary:
        if not self._db(self._db[self._tablename].id>0).count():
            self._db[self._tablename].insert(visits=self._initialVisits)
            pass
        pass

    def update(self):
        set=self._db(self._db[self._tablename].id==1)
        if not session.has_key('visits'):
            #session.visits = True
            newvisits = set.select()[0]['visits'] + 1
            set.update(visits=newvisits)
            session.visits = newvisits
            pass
        self.visits = session.visits
        pass

pageStatistics = PageStatistics(db, initialVisits=0)()

# or if you want to cheat:
##pageStatistics = PageStatistics(db, initialHits=16548, initialVisits=6541)()