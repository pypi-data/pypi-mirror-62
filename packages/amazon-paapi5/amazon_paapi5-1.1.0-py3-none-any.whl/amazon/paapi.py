"""
.. module:: paapi

"""

from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.api_client import ApiClient
from paapi5_python_sdk.configuration import Configuration
from paapi5_python_sdk.partner_type import PartnerType


from paapi5_python_sdk.rest import ApiException


from paapi5_python_sdk.get_items_request import GetItemsRequest
from paapi5_python_sdk.search_items_request import SearchItemsRequest
from paapi5_python_sdk.get_variations_request import GetVariationsRequest
from paapi5_python_sdk.get_browse_nodes_request import GetBrowseNodesRequest



import time, json, pickle, pprint
from urllib.parse import quote as urllib_quote
from .entities import AmazonProduct, AmazonBrowseNode
from .constant import *
from .exception import AmazonException



def _quote_query(query):
    """Turn a dictionary into a query string in a URL, with keys
    in alphabetical order."""
    return "&".join("%s=%s" % (
        k, urllib_quote(
            str(query[k]).encode('utf-8'), safe='~'))
            for k in sorted(query))

def parse_response_browse_node(browse_nodes_response_list):
    """
    The function parses Browse Nodes Response and creates a dict of BrowseNodeID to AmazonBrowseNode object

    params
        *browse_nodes_response_list*
            List of BrowseNodes in GetBrowseNodes response

    return
        Dict of BrowseNodeID to AmazonBrowseNode object

    """
    mapped_response = {}
    for browse_node in browse_nodes_response_list:
        mapped_response[browse_node.id] = browse_node
    return mapped_response


def parse_response_item(item_response_list):
    """
    The function parses GetItemsResponse and creates a dict of ASIN to AmazonProduct object

    params:
        *item_response_list*
            List of Items in GetItemsResponse

    return
        Dict of ASIN to AmazonProduct object
    """
    mapped_response = {}
    for item in item_response_list:
        mapped_response[item.asin] = item
    return mapped_response


class AmazonAPI:
    """
    Creates an instance containing your API credentials.

    params:
        *access_key (string)*
            Your API key
        *secret_key (string)*
            Your API secret
        *partner_tag (string)*
            The tag you want to use for the URL
        *country (string)*
            Country code
        *throttling (float, optional)*
            Reduce this value to wait longer between API calls
        *CacheReader (function)*
            Write a function to read the stored responses from previous api calls
        *CacheWriter (function)*
            Write a function to save the responses returned by amazon api calls
    
    
    """
    def __init__(self, access_key, secret_key, partner_tag, country='US', throttling=0.9, CacheReader=None, CacheWriter=None):
        """
            init AmazonApi. It is necessary to specify *access_key, secret_key, partner_tag, country* parameters
            By default the throttling parameter is set to 0.9. Increse or descrease this number to manage the time among different calls
            
            params:
                *access_key (string)*
                    amazon key of AWS account
                *secret_key (string)*
                    amazon secret of AWS account
                *partner_tag*
                    tag of the service Amazon Product Advertising account
                *country (string)*
                    possible values are defined in `amazon.constant.REGIONS`
                *throttling (float)*
                    value in the range (0,1] to wait among calls
                *CacheReader (function)*
                    function to read from cache 
                *CacheWriter (function)*
                    function to write results into the cache 

        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.partner_tag = partner_tag
        self.throttling = throttling
        self.country = country
        self.host = 'webservices.amazon.' + DOMAINS[country]
        self.region = REGIONS[country]
        self.marketplace = 'www.amazon.' + DOMAINS[country]
        self.last_query_time = time.time()
        self.CacheReader = CacheReader
        self.CacheWriter = CacheWriter

        self.default_api = DefaultApi(
            access_key=self.access_key, secret_key=self.secret_key, host=self.host, region=self.region
        )
        

    def _cache_url(self, query):
        """
            return a url used to identify the call and retrieve it from the cache if CacheReader and CacheWriter are set.
        """
        return self.host + "?" + _quote_query(query)



    
    def search_items(self, keywords, brand=None, condition=None, sortBy= None, browseNode=None, search_index="All", item_count=10, http_info=False, async_req=False, search_items_resource=SEARCH_RESOURCES):
        """ 
        Search products based on keywords
        Choose resources you want from SEARCH_RESOURCES enum 
        For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter 

        args:
            *keywords (string)*
                keywords to search products
            *brand* (string, optional)*
                filter the products based on the brand
            *condition* (enum, optional)*
                filter the products based on the condition
            *sortBy (string, optional)*
                sort hte results based on the specification defined at https://webservices.amazon.com/paapi5/documentation/search-items.html#sortby-parameter
            *browseNode (string)*
                search products into a specific browse node
            *search_index (string)*
                search products based on an index. Default value "All"
            *item_count (integer)*
                number of products returned. Values in the range [1,10]. Default 10
            *http_info (boolean)*
                specify if http header should be returned
            *async_req (boolean)*
                specify if a thread should be created to run the request
            *search_items_resource (list)*
                For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter. By deafult all possible resources are requested
        return
            Dict with 
                *data* 
                    contains the AmazonProduct list
                *http_info*
                    contains the http header information if requested. By default None
        """

        try:
            if keywords == '' or None:
                raise AmazonException("Keywords", "No keywords provided")
            if item_count > 10 or item_count < 1:
                item_count = 10
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'keywords':keywords,
                'search_index':search_index,
                'item_count':item_count,
                'condition':condition,
                'browse_node_id': browseNode,
                'brand': brand,
                'sort_by': sortBy  }
            )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return {'data': pickle.loads(cached_response_text['data']), 'http_info': pickle.loads(cached_response_text['http_info'])}

            search_items_request = SearchItemsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                keywords=keywords,
                search_index=search_index,
                item_count=item_count,
                resources=search_items_resource,
                condition=condition,
                browse_node_id=browseNode,
                brand=brand,
                sort_by=sortBy
            )
            
            
        except ValueError as exception:
            #print("Error in forming SearchItemsRequest: ", exception)
            raise AmazonException("ValueError", exception)
        except AmazonException as exception:
            #print("Error in forming SearchItemsRequest: ", exception)
            raise AmazonException(exception.status, exception.reason)

        try:
            """ Sending request """
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()
            resp_http = None
            if http_info:
                response_with_http_info = self.default_api.search_items_with_http_info(search_items_request)
                """ Parse response """
                if response_with_http_info is not None:
                    response = response_with_http_info[0]
                    resp_http = response_with_http_info[2]
                    if response.search_result is not None:
                        resp = [ AmazonProduct(item) for item in response.search_result.items]
                        if self.CacheWriter:
                            self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                        return {'data': resp, 'http_info': resp_http}
                    if response.errors is not None:
                        #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                        #print("Error code", response.errors[0].code)
                        #print("Error message", response.errors[0].message)
                        raise AmazonException(response.errors[0].code, response.errors[0].message)

            else:
                if async_req:
                    thread = self.default_api.search_items(search_items_request, async_req=True)
                    response = thread.get()
                else:
                    response = self.default_api.search_items(search_items_request)
                """ Parse response """
                if response.search_result is not None:
                    resp = [ AmazonProduct(item) for item in response.search_result.items]
                    if self.CacheWriter:
                        self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                    return {'data': resp, 'http_info': resp_http}
                if response.errors is not None:
                    #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    #print("Error code", response.errors[0].code)
                    #print("Error message", response.errors[0].message)
                    raise AmazonException(response.errors[0].code, response.errors[0].message)

        except ApiException as exception:
            #print("Error calling PA-API 5.0!")
            #print("Status code:", exception.status)
            #print("Errors :", exception.body)
            #print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise AmazonException("ApiException", exception.body)

        except TypeError as exception:
            #print("TypeError :", exception)
            raise AmazonException("TypeError", exception)

        except ValueError as exception:
            #print("ValueError :", exception)
            raise AmazonException(ValueError, exception)

        except AmazonException as exception:
            raise AmazonException(exception.status, exception.reason)
        
        except Exception as exception:
            raise AmazonException("General", exception)


    
    def search_items_pool(self, keywords, brand=None, condition=None, sortBy=None, browseNode=None, search_index="All", item_count=10, search_items_resource=SEARCH_RESOURCES ,connetion_pool_max_size=12):
        """ 
        Search products based on keywords. You can specify max connection pool size here. We recommend a value equal to cpu_count * 5.
        Choose resources you want from SEARCH_RESOURCES enum.
        For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter 

        args:
            *keywords (string)*
                keywords to search products
            *brand* (string, optional)*
                filter the products based on the brand
            *condition* (enum, optional)*
                filter the products based on the condition
            *sortBy (string, optional)*
                sort hte results based on the specification defined at https://webservices.amazon.com/paapi5/documentation/search-items.html#sortby-parameter
            *browseNode (string)*
                search products into a specific browse node
            *search_index (string)*
                search products based on an index. Default value "All"
            *item_count (integer)*
                number of products returned. Values in the range [1,10]. Default 10
            *search_items_resource (list)*
                For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter. By deafult all possible resources are requested
            *connetion_pool_max_size (integer)*
                sice of connection pool. Default 12
        return
            Dict with 
                *data* 
                    contains the AmazonProduct list
                *http_info*
                    contains the http header information if requested. By default None
        """
        
        configuration = Configuration()
        configuration.__init__(connetion_pool_max_size)

        """ API Client Declaration """
        api_client = ApiClient(
            access_key=self.access_key,
            secret_key=self.secret_key,
            host=self.host,
            region=self.region,
            configuration=configuration,
        )

        """ API declaration """
        default_api = DefaultApi(api_client=api_client)

        """ Forming request """
        try:
            if item_count > 10 or item_count < 1:
                item_count = 10

            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'keywords':keywords,
                'search_index':search_index,
                'item_count':item_count,
                'condition':condition,
                'browse_node_id': browseNode,
                'brand': brand,
                'sort_by': sortBy }
            )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return {'data': pickle.loads(cached_response_text['data']), 'http_info': pickle.loads(cached_response_text['http_info'])}

            search_items_request = SearchItemsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                keywords=keywords,
                search_index=search_index,
                item_count=item_count,
                resources=search_items_resource,
                condition=condition,
                browse_node_id=browseNode,
                brand=brand,
                sort_by=sortBy
            )
            

        except ValueError as exception:
            #print("Error in forming SearchItemsRequest: ", exception)
            raise AmazonException("ValueError", exception)

        try:
            """ Sending request """
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()
            resp_http = None
            response = default_api.search_items(search_items_request)

            """ Parse response """
            if response.search_result is not None:
                resp = [ AmazonProduct(item) for item in response.search_result.items]
                if self.CacheWriter:
                    self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                return {'data': resp, 'http_info': resp_http}
            if response.errors is not None:
                #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                #print("Error code", response.errors[0].code)
                #print("Error message", response.errors[0].message)
                raise AmazonException(response.errors[0].code, response.errors[0].message)

        except ApiException as exception:
            #print("Error calling PA-API 5.0!")
            #print("Status code:", exception.status)
            #print("Errors :", exception.body)
            #print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise AmazonException("ApiException", exception.body)

        except TypeError as exception:
            #print("TypeError :", exception)
            raise AmazonException("TypeError", exception)

        except ValueError as exception:
            #print("ValueError :", exception)
            raise AmazonException(ValueError, exception)

        except AmazonException as exception:
            raise AmazonException(exception.status, exception.reason)
        
        except Exception as exception:
            raise AmazonException("General", exception)
            raise Exception(exception)

    """ Choose resources you want from GetVariationsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-variations.html#resources-parameter """
    def get_variations(self, asin, condition=None, languages_of_preference=None, currency_of_preference=None, async_req=False, http_info=False, get_variations_resources=VARIATION_RESOURCES):
        """ 
        Get product variation using the asin of orginal product.
        Choose resources you want from VARIATION_RESOURCES enum.
        For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-variations.html#request-parameters

        args:
            *asin (string)*
                asin of the product for which we want the variations
            *condition* (enum, optional)*
                filter the products based on the condition
            *languages_of_preference (list of string)*
                specify the language of returned results
            *currency_of_preference (string)*
                specify the currency of returned results
            *http_info (boolean)*
                specify if http header should be returned
            *async_req (boolean)*
                specify if a thread should be created to run the request
            *get_variations_resources (list)*
                For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-variations.html#request-parameters. By deafult all possible resources are requested
            
        return
            Dict with 
                *data* 
                    contains the AmazonProduct list
                *http_info*
                    contains the http header information if requested. By default None
        """
        try:
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'asin':asin,
                'languages_of_preference':languages_of_preference,
                'condition': condition,
                'currency_of_preference': currency_of_preference
                }
            )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return {'data': pickle.loads(cached_response_text['data']), 'http_info': pickle.loads(cached_response_text['http_info'])}

            get_variations_request = GetVariationsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace=self.marketplace,
                languages_of_preference=languages_of_preference,
                asin=asin,
                resources=get_variations_resources,
                condition=condition,
                currency_of_preference=currency_of_preference
            )
            
        except ValueError as exception:
            #print("Error in forming GetVariationsRequest: ", exception)
            raise AmazonException("ValueError", exception)

        try:
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()
            resp_http = None
            """ Sending request """
            if http_info:
                response_with_http_info = self.default_api.get_variations_with_http_info(get_variations_request)

                """ Parse response """
                if response_with_http_info is not None:
                    response = response_with_http_info[0]
                    resp_http = response_with_http_info[2]
                    if response.variations_result is not None:
                        resp = [ AmazonProduct(item) for item in response.variations_result.items]
                        if self.CacheWriter:
                            self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                        return {'data': resp, 'http_info': resp_http}

                    if response.errors is not None:
                        #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                        #print("Error code", response.errors[0].code)
                        #print("Error message", response.errors[0].message)
                        raise AmazonException(response.errors[0].code, response.errors[0].message)
            else:
                if async_req:
                    thread = self.default_api.get_variations(get_variations_request, async_req=True)
                    response = thread.get()
                else:
                    response = self.default_api.get_variations(get_variations_request)

                """ Parse response """
                if response.variations_result is not None:
                    resp = [ AmazonProduct(item) for item in response.variations_result.items]
                    if self.CacheWriter:
                        self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                    return {'data': resp, 'http_info': resp_http}

                if response.errors is not None:
                    #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    #print("Error code", response.errors[0].code)
                    #print("Error message", response.errors[0].message)
                    raise AmazonException(response.errors[0].code, response.errors[0].message)

        except ApiException as exception:
            #print("Error calling PA-API 5.0!")
            #print("Status code:", exception.status)
            #print("Errors :", exception.body)
            #print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise AmazonException("ApiException", exception.body)

        except TypeError as exception:
            #print("TypeError :", exception)
            raise AmazonException("TypeError", exception)

        except ValueError as exception:
            #print("ValueError :", exception)
            raise AmazonException(ValueError, exception)

        except AmazonException as exception:
            raise AmazonException(exception.status, exception.reason)
        
        except Exception as exception:
            raise AmazonException("General", exception)


    """ Choose resources you want from GetItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-items.html#resources-parameter """
    def get_items(self, item_ids=[], currency_of_preference=None, condition=None, http_info=False, async_req=False, get_items_resource=ITEM_RESOURCES):
        """ 
        Get items' information.
        Choose resources you want from ITEM_RESOURCES enum 
        For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-items.html#ItemLookup-rp

        args:
            *item_ids (list of string)*
                list of asin of the products of interest
            *currency_of_preference (string)*
                specify the currency of returned results
            *condition* (enum, optional)*
                filter the products based on the condition
            *http_info (boolean)*
                specify if http header should be returned
            *async_req (boolean)*
                specify if a thread should be created to run the request
            *get_items_resource (list)*
                For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-items.html#ItemLookup-rp. By deafult all possible resources are requested
            
        return
            Dict with 
                *data* 
                    Dict of ASIN to AmazonProduct object
                *http_info*
                    contains the http header information if requested. By default None
        """
        
        if len(item_ids) == 0:
            raise Exception('No item ids specified')
        
        """ Forming request """
        try:
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'item_ids':item_ids,
                'condition':condition,
                'currency_of_preference': currency_of_preference  }
                )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return {'data': parse_response_item( pickle.loads(cached_response_text['data']) ), 'http_info': pickle.loads(cached_response_text['http_info'])}

            get_items_request = GetItemsRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace=self.marketplace,
                condition=condition,
                item_ids=item_ids,
                resources=get_items_resource,
                currency_of_preference=currency_of_preference
            )
            

        except ValueError as exception:
            #print("Error in forming GetItemsRequest: ", exception)
            raise AmazonException("ValueError", exception)

        try:
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()
            resp_http = None

            if http_info:
                response_with_http_info = self.default_api.get_items_with_http_info(
                    get_items_request
                )

                """ Parse response """
                if response_with_http_info is not None:
                    response = response_with_http_info[0]
                    resp_http = response_with_http_info[2]
                    if response.items_result is not None:
                        resp = [ AmazonProduct(item) for item in response.items_result.items]
                        if self.CacheWriter:
                            self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                        return {'data': parse_response_item(resp), 'http_info': resp_http}
                        
                    if response.errors is not None:
                        #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                        #print("Error code", response.errors[0].code)
                        #print("Error message", response.errors[0].message)
                        raise AmazonException(response.errors[0].code, response.errors[0].message)

            else:
                """ Sending request """
                if async_req:
                    thread = self.default_api.get_items(get_items_request, async_req=True)
                    response = thread.get()
                else:
                    response = self.default_api.get_items(get_items_request)

                """ Parse response """
                if response.items_result is not None:
                    resp = [ AmazonProduct(item) for item in response.items_result.items]
                    if self.CacheWriter:
                        self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                    return {'data': parse_response_item(resp), 'http_info': resp_http}

                if response.errors is not None:
                    #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    #print("Error code", response.errors[0].code)
                    #print("Error message", response.errors[0].message)
                    raise AmazonException(response.errors[0].code, response.errors[0].message)


        except ApiException as exception:
            #print("Error calling PA-API 5.0!")
            #print("Status code:", exception.status)
            #print("Errors :", exception.body)
            #print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise AmazonException("ApiException", exception.body)

        except TypeError as exception:
            #print("TypeError :", exception)
            raise AmazonException("TypeError", exception)

        except ValueError as exception:
            #print("ValueError :", exception)
            raise AmazonException(ValueError, exception)

        except AmazonException as exception:
            raise AmazonException(exception.status, exception.reason)
        
        except Exception as exception:
            raise AmazonException("General", exception)



    """ Choose resources you want from GetBrowseNodesResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/getbrowsenodes.html#resources-parameter """
    def get_browse_nodes(self, browse_node_ids=[], http_info=False, async_req=False, languages_of_preference = None, get_browse_node_resources=BROWSE_RESOURCES):
        """" 
        Get browse nodes' information.
        Choose resources you want from BROWSE_RESOURCES enum 
        For more details, refer: https://webservices.amazon.com/paapi5/documentation/getbrowsenodes.html#request-parameters

        args:
            *browse_node_ids (list of string)*
                list of browse node ids
            *http_info (boolean)*
                specify if http header should be returned
            *async_req (boolean)*
                specify if a thread should be created to run the request
            *languages_of_preference (list of string)*
                specify the language of returned results
            *get_browse_node_resources (list)*
                For more details, refer: https://webservices.amazon.com/paapi5/documentation/getbrowsenodes.html#request-parameters. By deafult all possible resources are requested
            
        return
            Dict with 
                *data* 
                    Dict of BrowseNodeID to AmazonBrowseNode object
                *http_info*
                    contains the http header information if requested. By default None
        """
        
        if isinstance(browse_node_ids, list) == False or len (browse_node_ids) == 0:
            raise Exception('Browse node ids are not in the right format')
        
        """ Forming request """
        try:
            cache_url = self._cache_url(
                {'partner_tag':self.partner_tag,
                'partner_type':PartnerType.ASSOCIATES,
                'browse_node_ids':browse_node_ids,
                'languages_of_preference':languages_of_preference }
                )
            
            if self.CacheReader:
                cached_response_text = self.CacheReader(cache_url)
                if cached_response_text is not None:
                    return {'data': parse_response_browse_node (pickle.loads(cached_response_text['data']) ), 'http_info': pickle.loads(cached_response_text['http_info'])}

            get_browse_node_request = GetBrowseNodesRequest(
                partner_tag=self.partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace=self.marketplace,
                languages_of_preference=languages_of_preference,
                browse_node_ids=browse_node_ids,
                resources=get_browse_node_resources,
            )
            
        except ValueError as exception:
            #print("Error in forming GetBrowseNodesRequest: ", exception)
            raise AmazonException("ValueError", exception)

        try:
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()
            resp_http = None

            if http_info:
                response_with_http_info = self.default_api.get_browse_nodes_with_http_info(get_browse_node_request)

                """ Parse response """
                if response_with_http_info is not None:
                    response = response_with_http_info[0]
                    resp_http = response_with_http_info[2]
                    if response.browse_nodes_result is not None:
                        resp = [ AmazonBrowseNode(node) for node in response.browse_nodes_result.browse_nodes]
                        if self.CacheWriter:
                            self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                        return {'data': parse_response_browse_node(resp), 'http_info': resp_http}
                        
                    if response.errors is not None:
                        #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                        #print("Error code", response.errors[0].code)
                        #print("Error message", response.errors[0].message)
                        raise AmazonException(response.errors[0].code, response.errors[0].message)

            else:
                """ Sending request """
                if async_req:
                    thread = self.default_api.get_browse_nodes(get_browse_node_request, async_req=True)
                    response = thread.get()
                else:
                    response = self.default_api.get_browse_nodes(get_browse_node_request)

                """ Parse response """
                if response.browse_nodes_result is not None:
                    resp = [ AmazonBrowseNode(item) for item in response.browse_nodes_result.browse_nodes]
                    if self.CacheWriter:
                        self.CacheWriter(cache_url, pickle.dumps(resp), pickle.dumps(resp_http))
                    return {'data': parse_response_browse_node(resp), 'http_info': resp_http}
                    
                if response.errors is not None:
                    #print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                    #print("Error code", response.errors[0].code)
                    #print("Error message", response.errors[0].message)
                    raise AmazonException(response.errors[0].code, response.errors[0].message)

        except ApiException as exception:
            #print("Error calling PA-API 5.0!")
            #print("Status code:", exception.status)
            #print("Errors :", exception.body)
            #print("Request ID:", exception.headers["x-amzn-RequestId"])
            raise AmazonException("ApiException", exception.body)

        except TypeError as exception:
            #print("TypeError :", exception)
            raise AmazonException("TypeError", exception)

        except ValueError as exception:
            #print("ValueError :", exception)
            raise AmazonException(ValueError, exception)

        except AmazonException as exception:
            raise AmazonException(exception.status, exception.reason)
        
        except Exception as exception:
            raise AmazonException("General", exception)
