# -*- coding: utf-8 -*-
#
# Copyright 2020 by Hartmut Goebel <h.goebel@crazy-compilers.com>
#
# This file is part of flyer-composer.
#
# flyer-composer is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# flyer-composer is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with flyer-composer. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Build requirements
# - ImageMagick
#

images = projectlogo.png projecticon.ico projecticon.png

all: $(images)

projectlogo.png: projectlogo-fullcolor.svg
	convert $< -resize 100x100 $@

projecticon.ico: projecticon-fullcolor.svg
	convert -background none $< -define "icon:auto-resize=256,128,64,48,32" $@

projecticon.png: projecticon-fullcolor.svg
	convert -background none $< -resize 100x100 $@

clean:
	rm -f $(images)
