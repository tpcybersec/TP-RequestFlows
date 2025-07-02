TP_RequestFlows_VERSION = "2025.7.1"

from TP_Requests.http import TP_HTTP_REQUEST
from TP_HTTP_Request_Response_Parser import TP_HTTP_REQUEST_PARSER, TP_HTTP_RESPONSE_PARSER
import json_duplicate_keys as jdks
import glob, os, datetime, re, time


AUTO_LOGIN = dict()

def run_flows(FlowFolder, add_object=dict(), update_object=dict(), delete_object=dict(), ReqTimeout=60, ReqDelaytime=0, sleeptime=20, separator="||", parse_index="$", dupSign_start="{{{", dupSign_end="}}}", ordered_dict=False, skipDuplicated=True, update_content_length=True, proxy_server=None, verbose=True):
	Flows = dict()

	def kwvars(Flows, environments):
		vars = dict()

		for importLib in environments["libs"]: exec(importLib)

		for name in environments["vars"]:
			if environments["vars"][name]["runCode"]:
				try:
					vars[name] = "JSON_DUPLICATE_KEYS_ERROR"
					if "LOOPVAR" in environments["vars"][name] and "CONDITION" in environments["vars"][name]:
						for LOOPDATA in eval(environments["vars"][name]["LOOPVAR"]):
							if eval(environments["vars"][name]["CONDITION"]):
								vars[name] = eval(environments["vars"][name]["value"])
								break
					else:
						vars[name] = eval(environments["vars"][name]["value"])
				except Exception as e:
					pass
			else:
				vars[name] = environments["vars"][name]["value"]

		return vars


	RequestRules = jdks.load(os.path.join(FlowFolder, "rules.json"), _isDebug_=True)

	total_rawReq = len(glob.glob1(FlowFolder, "raw-[0-9]*.req"))
	i = 0
	while i < total_rawReq:
		reqNum = str(i+1)

		Coding = "utf-8"
		try:
			Coding = RequestRules.get("flows")["value"][reqNum]["Coding"]
		except Exception as e:
			pass

		rawRequest = open(os.path.join(FlowFolder, "raw-{}.req".format(reqNum)), encoding=Coding).read()

		req = TP_HTTP_REQUEST(rawRequest, Coding, separator=separator, parse_index=parse_index, dupSign_start=dupSign_start, dupSign_end=dupSign_end, ordered_dict=ordered_dict, skipDuplicated=skipDuplicated)

		if "PathParams" in RequestRules.get("flows"+separator+reqNum)["value"]:
			PathParams = RequestRules.get("flows"+separator+reqNum+separator+"PathParams")["value"]
			if type(PathParams) == dict:
				for name in PathParams:
					try:
						if PathParams[name].split("||",1)[0] == "AUTO_LOGIN":
							value = AUTO_LOGIN[PathParams[name].split("||",1)[1]]
						else:
							value = PathParams[name].format(**kwvars(Flows, RequestRules.get("environments")["value"]))
							if "JSON_DUPLICATE_KEYS_ERROR" in value:
								if verbose: print(f"\x1b[31m[-] Could not get the {PathParams[name]} value for next request\x1b[0m")
								return {
									"flow": False,
									"success": False,
									"data": Flows
								}

						req.RequestParser.request_pathParams.update(name, value)
					except Exception as e:
						pass

		if "QueryParams" in RequestRules.get("flows"+separator+reqNum)["value"]:
			QueryParams = RequestRules.get("flows"+separator+reqNum+separator+"QueryParams")["value"]
			if type(QueryParams) == dict:
				for name in QueryParams:
					try:
						if QueryParams[name].split("||",1)[0] == "AUTO_LOGIN":
							value = AUTO_LOGIN[QueryParams[name].split("||",1)[1]]
						else:
							value = QueryParams[name].format(**kwvars(Flows, RequestRules.get("environments")["value"]))
							if "JSON_DUPLICATE_KEYS_ERROR" in value:
								if verbose: print(f"\x1b[31m[-] Could not get the {QueryParams[name]} value for next request\x1b[0m")
								return {
									"flow": False,
									"success": False,
									"data": Flows
								}

						req.RequestParser.request_queryParams.update(name, value)
					except Exception as e:
						pass

		if "HTTPHeaders" in RequestRules.get("flows"+separator+reqNum)["value"]:
			HTTPHeaders = RequestRules.get("flows"+separator+reqNum+separator+"HTTPHeaders")["value"]
			if type(HTTPHeaders) == dict:
				for name in HTTPHeaders:
					try:
						if HTTPHeaders[name].split("||",1)[0] == "AUTO_LOGIN":
							value = AUTO_LOGIN[HTTPHeaders[name].split("||",1)[1]]
						else:
							value = HTTPHeaders[name].format(**kwvars(Flows, RequestRules.get("environments")["value"]))
							if "JSON_DUPLICATE_KEYS_ERROR" in value:
								if verbose: print(f"\x1b[31m[-] Could not get the {HTTPHeaders[name]} value for next request\x1b[0m")
								return {
									"flow": False,
									"success": False,
									"data": Flows
								}

						req.RequestParser.request_headers.update(name, value)
					except Exception as e:
						pass

		if "HTTPCookies" in RequestRules.get("flows"+separator+reqNum)["value"]:
			HTTPCookies = RequestRules.get("flows"+separator+reqNum+separator+"HTTPCookies")["value"]
			if type(HTTPCookies) == dict:
				for name in HTTPCookies:
					try:
						if HTTPCookies[name].split("||",1)[0] == "AUTO_LOGIN":
							value = AUTO_LOGIN[HTTPCookies[name].split("||",1)[1]]
						else:
							value = HTTPCookies[name].format(**kwvars(Flows, RequestRules.get("environments")["value"]))
							if "JSON_DUPLICATE_KEYS_ERROR" in value:
								if verbose: print(f"\x1b[31m[-] Could not get the {HTTPCookies[name]} value for next request\x1b[0m")
								return {
									"flow": False,
									"success": False,
									"data": Flows
								}

						req.RequestParser.request_cookies.update(name, value)
					except Exception as e:
						pass

		if "RequestBody" in RequestRules.get("flows"+separator+reqNum)["value"]:
			RequestBody = RequestRules.get("flows"+separator+reqNum+separator+"RequestBody")["value"]
			if type(RequestBody) == dict:
				for name in RequestBody:
					try:
						if RequestBody[name].split("||",1)[0] == "AUTO_LOGIN":
							value = AUTO_LOGIN[RequestBody[name].split("||",1)[1]]
						else:
							value = RequestBody[name].format(**kwvars(Flows, RequestRules.get("environments")["value"]))
							if "JSON_DUPLICATE_KEYS_ERROR" in value:
								if verbose: print(f"\x1b[31m[-] Could not get the {RequestBody[name]} value for next request\x1b[0m")
								return {
									"flow": False,
									"success": False,
									"data": Flows
								}

						try:
							datetype_ori = type(req.RequestParser.request_body.get("data"+separator+name)["value"])
							datatype_new = type(eval(value))

							if datetype_ori == datatype_new or datetype_ori in [int, float] and datatype_new in [int, float] or type(eval(value)) == bytes:
								req.RequestParser.request_body.update("data"+separator+name, eval(value))
							else:
								req.RequestParser.request_body.update("data"+separator+name, value)
						except Exception as e:
							req.RequestParser.request_body.update("data"+separator+name, value)
					except Exception as e:
						pass
			else:
				req.RequestParser.request_body.update("data", str(RequestBody).format(**kwvars(Flows, RequestRules.get("environments")["value"])))
				req.RequestParser.request_body.update("dataType", "unknown")


		if reqNum in add_object:
			for obj in add_object[reqNum]:
				if obj == "QueryParams" and type(add_object[reqNum]["QueryParams"]) == dict:
					for name in add_object[reqNum]["QueryParams"]:
						req.RequestParser.request_queryParams.set(name, add_object[reqNum]["QueryParams"][name])
				
				if obj == "HTTPHeaders" and type(add_object[reqNum]["HTTPHeaders"]) == dict:
					for name in add_object[reqNum]["HTTPHeaders"]:
						req.RequestParser.request_headers.set(name, add_object[reqNum]["HTTPHeaders"][name])
				
				if obj == "HTTPCookies" and type(add_object[reqNum]["HTTPCookies"]) == dict:
					for name in add_object[reqNum]["HTTPCookies"]:
						req.RequestParser.request_cookies.set(name, add_object[reqNum]["HTTPCookies"][name])

				if obj == "RequestBody" and type(add_object[reqNum]["RequestBody"]) == dict:
					for name in add_object[reqNum]["RequestBody"]:
						req.RequestParser.request_body.set("data"+separator+name, add_object[reqNum]["RequestBody"][name])


		if reqNum in update_object:
			for obj in update_object[reqNum]:
				if obj == "RequestMethod":
					req.RequestParser.request_method = str(update_object[reqNum]["RequestMethod"])
				
				if obj == "RequestPath":
					req.RequestParser.request_path = str(update_object[reqNum]["RequestPath"])

				if obj == "PathParams" and type(update_object[reqNum]["PathParams"]) == dict:
					for name in update_object[reqNum]["PathParams"]:
						req.RequestParser.request_pathParams.update(name, update_object[reqNum]["PathParams"][name])

				if obj == "QueryParams" and type(update_object[reqNum]["QueryParams"]) == dict:
					for name in update_object[reqNum]["QueryParams"]:
						req.RequestParser.request_queryParams.update(name, update_object[reqNum]["QueryParams"][name])

				if obj == "RequestFragment":
					req.RequestParser.request_fragment = str(update_object[reqNum]["RequestFragment"])
				
				if obj == "HTTPVersion":
					req.RequestParser.request_httpVersion = str(update_object[reqNum]["HTTPVersion"])

				if obj == "HTTPHeaders" and type(update_object[reqNum]["HTTPHeaders"]) == dict:
					for name in update_object[reqNum]["HTTPHeaders"]:
						req.RequestParser.request_headers.update(name, update_object[reqNum]["HTTPHeaders"][name])
				
				if obj == "HTTPCookies" and type(update_object[reqNum]["HTTPCookies"]) == dict:
					for name in update_object[reqNum]["HTTPCookies"]:
						req.RequestParser.request_cookies.update(name, update_object[reqNum]["HTTPCookies"][name])
				
				if obj == "RequestBody":
					if type(update_object[reqNum]["RequestBody"]) == dict:
						for name in update_object[reqNum]["RequestBody"]:
							req.RequestParser.request_body.update("data"+separator+name, update_object[reqNum]["RequestBody"][name])
					else:
						req.RequestParser.request_body.update("data", str(update_object[reqNum]["RequestBody"][name]))


		if reqNum in delete_object:
			for obj in delete_object[reqNum]:
				if obj == "QueryParams" and type(delete_object[reqNum]["QueryParams"]) == list:
					for name in delete_object[reqNum]["QueryParams"]:
						req.RequestParser.request_queryParams.delete(name)
				
				if obj == "HTTPHeaders" and type(delete_object[reqNum]["HTTPHeaders"]) == list:
					for name in delete_object[reqNum]["HTTPHeaders"]:
						req.RequestParser.request_headers.delete(name)
				
				if obj == "HTTPCookies" and type(delete_object[reqNum]["HTTPCookies"]) == list:
					for name in delete_object[reqNum]["HTTPCookies"]:
						req.RequestParser.request_cookies.delete(name)
				
				if obj == "RequestBody" and type(delete_object[reqNum]["RequestBody"]) == list:
					for name in delete_object[reqNum]["RequestBody"]:
						req.RequestParser.request_body.delete("data"+separator+name)


		Scheme = RequestRules.get("flows")["value"][reqNum]["Scheme"]
		Host = RequestRules.get("flows")["value"][reqNum]["Host"]
		Port = RequestRules.get("flows")["value"][reqNum]["Port"]
		Flows[reqNum] = req.sendRequest(Host, Port, Scheme, ReqTimeout=ReqTimeout, update_content_length=update_content_length, proxy_server=proxy_server)

		if verbose:
			ResponseParser = TP_HTTP_RESPONSE_PARSER(Flows[reqNum]["rawResponse"], separator=separator, parse_index=parse_index, dupSign_start=dupSign_start, dupSign_end=dupSign_end, ordered_dict=ordered_dict, skipDuplicated=skipDuplicated)

			if req.RequestParser.request_method.upper() == "GET":
				RequestMethod = f"\x1b[30;42m {req.RequestParser.request_method} \x1b[0m"
			elif req.RequestParser.request_method.upper() == "POST":
				RequestMethod = f"\x1b[30;46m {req.RequestParser.request_method} \x1b[0m"
			elif req.RequestParser.request_method.upper() == "PUT":
				RequestMethod = f"\x1b[30;43m {req.RequestParser.request_method} \x1b[0m"
			elif req.RequestParser.request_method.upper() == "DELETE":
				RequestMethod = f"\x1b[30;41m {req.RequestParser.request_method} \x1b[0m"
			elif req.RequestParser.request_method.upper() == "PATCH":
				RequestMethod = f"\x1b[30;45m {req.RequestParser.request_method} \x1b[0m"
			elif req.RequestParser.request_method.upper() == "OPTIONS":
				RequestMethod = f"\x1b[30;44m {req.RequestParser.request_method} \x1b[0m"
			elif req.RequestParser.request_method.upper() == "HEAD":
				RequestMethod = f"\x1b[30;47m {req.RequestParser.request_method} \x1b[0m"
			else:
				RequestMethod = f"\x1b[30;107m {req.RequestParser.request_method} \x1b[0m"

			if type(ResponseParser.response_statusCode) == int:
				if 100 <= ResponseParser.response_statusCode < 200:
					Response_Status = f"| \x1b[34m{ResponseParser.response_statusCode} {ResponseParser.response_statusText} \x1b[0m"
				elif 200 <= ResponseParser.response_statusCode < 300:
					Response_Status = f"| \x1b[32m{ResponseParser.response_statusCode} {ResponseParser.response_statusText} \x1b[0m"
				elif 300 <= ResponseParser.response_statusCode < 400:
					Response_Status = f"| \x1b[36m{ResponseParser.response_statusCode} {ResponseParser.response_statusText} \x1b[0m"
				elif 400 <= ResponseParser.response_statusCode < 500:
					Response_Status = f"| \x1b[33m{ResponseParser.response_statusCode} {ResponseParser.response_statusText} \x1b[0m"
				elif 500 <= ResponseParser.response_statusCode < 600:
					Response_Status = f"| \x1b[31m{ResponseParser.response_statusCode} {ResponseParser.response_statusText} \x1b[0m"
				else:
					Response_Status = f"| \x1b[37m{ResponseParser.response_statusCode} {ResponseParser.response_statusText} \x1b[0m"
			else:
				Response_Status = f"| \x1b[37m{ResponseParser.response_statusCode} {ResponseParser.response_statusText} \x1b[0m"

			RequestTime = f"| RT: {Flows[reqNum]['RequestTime']}ms"
			if Flows[reqNum]['RequestTime'] >= sleeptime * 1000 or Flows[reqNum]['RequestTime'] < 0: RequestTime = f"| \x1b[1;31mRT: {Flows[reqNum]['RequestTime']}ms\x1b[0m"

			print(f"[\x1b[34m{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\x1b[0m] " +
				RequestMethod + " " +
				f"\x1b[32m{f'{Scheme}://{Host}' if (Scheme=='https' and Port==443) or (Scheme=='http' and Port==80) else f'{Scheme}://{Host}:{Port}'}" +
				re.split("\r\n|\n", re.split("\r\n\r\n|\n\n", Flows[reqNum]["rawRequest"], 1)[0])[0].split(" ")[1] + "\x1b[0m " +
				Response_Status +
				f"| CL: {ResponseParser.response_headers.get('Content-Length', case_insensitive=True)['value']} " +
				RequestTime
			)

		# AUTO LOGIN
		if RequestRules.get("AutoLogin||Matcher")["value"] != "JSON_DUPLICATE_KEYS_ERROR":
			flag_AutoLogin = False
			CONDITION = RequestRules.get("AutoLogin||Matcher||CONDITION")["value"]
			if CONDITION == "OR":
				flag_AutoLogin = False
				for pattern in RequestRules.get("AutoLogin||Matcher||PATTERN")["value"]:
					if type(Flows[reqNum]["rawResponse"]) == bytes:
						pattern = pattern.encode()

					if re.search(pattern, Flows[reqNum]["rawResponse"]):
						flag_AutoLogin = True
						break
			elif CONDITION == "AND":
				flag_AutoLogin = True
				for pattern in RequestRules.get("AutoLogin||Matcher||PATTERN")["value"]:
					if type(Flows[reqNum]["rawResponse"]) == bytes:
						pattern = pattern.encode()

					if not re.search(pattern, Flows[reqNum]["rawResponse"]):
						flag_AutoLogin = False
						break

			if flag_AutoLogin:
				run_results = run_flows(RequestRules.get("AutoLogin||ObtainSessionTokenFlow")["value"], ReqTimeout=ReqTimeout, ReqDelaytime=ReqDelaytime, sleeptime=sleeptime, separator=separator, parse_index=parse_index, dupSign_start=dupSign_start, dupSign_end=dupSign_end, ordered_dict=ordered_dict, proxy_server=proxy_server)
				if run_results["flow"] and run_results["success"]:
					Flows_AutoLogin = run_results["data"]
					for k,v in RequestRules.get("AutoLogin||Extractors")["value"].items():
						AUTO_LOGIN[k] = eval(v)
					i -= 1
					reqNum = str(i+1)
				else:
					return {
						"flow": False,
						"success": False,
						"data": Flows
					}

		if reqNum == str(total_rawReq) and RequestRules.get("PATTERN_SuccessFlows")["value"] != "JSON_DUPLICATE_KEYS_ERROR" and type(RequestRules.get("PATTERN_SuccessFlows")["value"]) == str:
			PATTERN_SuccessFlows = RequestRules.get("PATTERN_SuccessFlows")["value"]
			if type(Flows[reqNum]["rawResponse"]) == bytes:
				PATTERN_SuccessFlows = PATTERN_SuccessFlows.encode()

			if not re.search(PATTERN_SuccessFlows, Flows[reqNum]["rawResponse"]):
				if verbose: print("\x1b[1;31m[-] THE REQUEST FLOW HAS NOT BEEN COMPLETED SUCCESSFULLY. PLEASE CHECK AGAIN.\x1b[0m")
				return {
					"flow": True,
					"success": False,
					"data": Flows
				}

			if verbose: print("\x1b[1;34m[+] THE REQUEST FLOW HAS BEEN COMPLETED SUCCESSFULLY.\x1b[0m")

		time.sleep(ReqDelaytime)
		i += 1

	return {
		"flow": True,
		"success": True,
		"data": Flows
	}