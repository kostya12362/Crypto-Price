#!/bin/bash
aerich init -t models.__init__.TORTOISE_ORM
aerich init-db
aerich migrate
aerich upgrade
