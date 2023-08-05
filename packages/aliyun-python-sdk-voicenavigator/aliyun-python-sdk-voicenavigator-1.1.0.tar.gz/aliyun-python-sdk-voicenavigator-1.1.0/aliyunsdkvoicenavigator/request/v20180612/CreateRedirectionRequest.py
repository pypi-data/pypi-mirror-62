# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkvoicenavigator.endpoint import endpoint_data

class CreateRedirectionRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'VoiceNavigator', '2018-06-12', 'CreateRedirection','voicebot')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_RedirectionType(self):
		return self.get_query_params().get('RedirectionType')

	def set_RedirectionType(self,RedirectionType):
		self.add_query_param('RedirectionType',RedirectionType)

	def get_UserUtterance(self):
		return self.get_query_params().get('UserUtterance')

	def set_UserUtterance(self,UserUtterance):
		self.add_query_param('UserUtterance',UserUtterance)

	def get_Interruptible(self):
		return self.get_query_params().get('Interruptible')

	def set_Interruptible(self,Interruptible):
		self.add_query_param('Interruptible',Interruptible)

	def get_InstanceId(self):
		return self.get_query_params().get('InstanceId')

	def set_InstanceId(self,InstanceId):
		self.add_query_param('InstanceId',InstanceId)

	def get_SimilarUtterancess(self):
		return self.get_query_params().get('SimilarUtterancess')

	def set_SimilarUtterancess(self,SimilarUtterancess):
		for i in range(len(SimilarUtterancess)):	
			if SimilarUtterancess[i] is not None:
				self.add_query_param('SimilarUtterances.' + str(i + 1) , SimilarUtterancess[i]);

	def get_RedirectionTarget(self):
		return self.get_query_params().get('RedirectionTarget')

	def set_RedirectionTarget(self,RedirectionTarget):
		self.add_query_param('RedirectionTarget',RedirectionTarget)

	def get_Prompt(self):
		return self.get_query_params().get('Prompt')

	def set_Prompt(self,Prompt):
		self.add_query_param('Prompt',Prompt)

	def get_CategoryId(self):
		return self.get_query_params().get('CategoryId')

	def set_CategoryId(self,CategoryId):
		self.add_query_param('CategoryId',CategoryId)