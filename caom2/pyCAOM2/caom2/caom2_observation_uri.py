#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#***********************************************************************
#******************  CANADIAN ASTRONOMY DATA CENTRE  *******************
#*************  CENTRE CANADIEN DE DONNÉES ASTRONOMIQUES  **************
#
#  (c) 2010.                            (c) 2010.
#  Government of Canada                 Gouvernement du Canada
#  National Research Council            Conseil national de recherches
#  Ottawa, Canada, K1A 0R6              Ottawa, Canada, K1A 0R6
#  All rights reserved                  Tous droits réservés
#                                       
#  NRC disclaims any warranties,        Le CNRC dénie toute garantie
#  expressed, implied, or               énoncée, implicite ou légale,
#  statutory, of any kind with          de quelque nature que ce
#  respect to the software,             soit, concernant le logiciel,
#  including without limitation         y compris sans restriction
#  any warranty of merchantability      toute garantie de valeur
#  or fitness for a particular          marchande ou de pertinence
#  purpose. NRC shall not be            pour un usage particulier.
#  liable in any event for any          Le CNRC ne pourra en aucun cas
#  damages, whether direct or           être tenu responsable de tout
#  indirect, special or general,        dommage, direct ou indirect,
#  consequential or incidental,         particulier ou général,
#  arising from the use of the          accessoire ou fortuit, résultant
#  software.  Neither the name          de l'utilisation du logiciel. Ni
#  of the National Research             le nom du Conseil National de
#  Council of Canada nor the            Recherches du Canada ni les noms
#  names of its contributors may        de ses  participants ne peuvent
#  be used to endorse or promote        être utilisés pour approuver ou
#  products derived from this           promouvoir les produits dérivés
#  software without specific prior      de ce logiciel sans autorisation
#  written permission.                  préalable et particulière
#                                       par écrit.
#                                       
#  This file is part of the             Ce fichier fait partie du projet
#  OpenCADC project.                    OpenCADC.
#                                       
#  OpenCADC is free software:           OpenCADC est un logiciel libre ;
#  you can redistribute it and/or       vous pouvez le redistribuer ou le
#  modify it under the terms of         modifier suivant les termes de
#  the GNU Affero General Public        la “GNU Affero General Public
#  License as published by the          License” telle que publiée
#  Free Software Foundation,            par la Free Software Foundation
#  either version 3 of the              : soit la version 3 de cette
#  License, or (at your option)         licence, soit (à votre gré)
#  any later version.                   toute version ultérieure.
#                                       
#  OpenCADC is distributed in the       OpenCADC est distribué
#  hope that it will be useful,         dans l’espoir qu’il vous
#  but WITHOUT ANY WARRANTY;            sera utile, mais SANS AUCUNE
#  without even the implied             GARANTIE : sans même la garantie
#  warranty of MERCHANTABILITY          implicite de COMMERCIALISABILITÉ
#  or FITNESS FOR A PARTICULAR          ni d’ADÉQUATION À UN OBJECTIF
#  PURPOSE.  See the GNU Affero         PARTICULIER. Consultez la Licence
#  General Public License for           Générale Publique GNU Affero
#  more details.                        pour plus de détails.
#                                       
#  You should have received             Vous devriez avoir reçu une
#  a copy of the GNU Affero             copie de la Licence Générale
#  General Public License along         Publique GNU Affero avec
#  with OpenCADC.  If not, see          OpenCADC ; si ce n’est
#  <http://www.gnu.org/licenses/>.      pas le cas, consultez :
#                                       <http://www.gnu.org/licenses/>.
#
#  $Revision: 4 $
#
#***********************************************************************
#

""" defines the ObservationURI class """


from util.caom2_util import validate_path_component
from urlparse import urlsplit
from urlparse import SplitResult
from util import caom2_util as util
from caom2_object import Caom2Object

class ObservationURI(Caom2Object):
    """ Observation URI """

    _SCHEME = str("caom")

    def __init__(self, uri):
        """
        Initializes an Observation instance

        Arguments:
        uri : URI corresponding to observation
        """
        tmp = urlsplit(uri)
        
        if tmp.scheme != ObservationURI._SCHEME:
            raise ValueError(
                "uri must be have scheme of {}. received: {}".format(ObservationURI._SCHEME, 
                                                                     uri))
        if tmp.geturl() != uri:
            raise ValueError(
                "uri parsing failure.  received: {}".format(uri))

        self._uri = tmp.geturl()
        (collection, observation_id) = tmp.path.split("/")
        if collection is  None:
            raise ValueError(
                "uri did not contain a collection part. received: {}".format(uri))
        validate_path_component(self, "collection", collection)
        if observation_id is None:
            raise ValueError(
                "uri did not contain an observation_id part. received: {}".format(uri))
        validate_path_component(self,"observation_id", observation_id)
        (self._collection, self._observation_id) = (collection, observation_id)
        self._print_attributes = ['uri', 'collection', 'observation_id']

    def _key(self):
        return (self.uri)

    def __eq__(self, y):
        if (isinstance(y, ObservationURI)):
            return self._key() == y._key()
        return False

    def __hash__(self):
        return hash(self._key())

    @classmethod
    def get_observation_uri(cls, collection, observation_id):
        """
        Initializes an Observation URI instance

        Arguments:
        collection : collection
        observation_id : ID of the observation
        """

        util.typeCheck(collection, str, "collection", override=False)
        util.typeCheck(observation_id, str, "observation_id", override=False)

        validate_path_component(cls, "collection", collection)
        validate_path_component(cls, "observation_id",
                                           observation_id)

        uri = SplitResult(ObservationURI._SCHEME, "", collection + "/" +
                          observation_id, "", "").geturl()
        return cls(uri)

    # Properties

    @property
    @classmethod
    def SCHEME(cls):
        """The SCHEME defines where this Observation can be looked up. 

        Only 'caom' is currently supported."""
        return cls._SCHEME

    @property
    def uri(self):
        """The uri that the caom service can use to find the observation"""
        return self._uri

    @property
    def collection(self):
        """The collection part of this Observations uri"""
        return self._collection

    @property
    def observation_id(self):
        """The observation_id of this Observations uri"""
        return self._observation_id