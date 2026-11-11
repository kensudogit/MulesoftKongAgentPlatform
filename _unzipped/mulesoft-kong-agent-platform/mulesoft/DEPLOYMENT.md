# MuleSoft deployment preparation

1. Confirm Anypoint subscription, Mule runtime version, Runtime Manager/CloudHub 2.0 vs Runtime Fabric vs on-premises choice, connectivity and allowed connectors.
2. Create dev/test/prod environments and RBAC; connect a secure secret store and approved network path to internal systems.
3. Create Mule 4 project with required HTTP and EE modules, build with Mule Maven Plugin and deploy via CI; sample-flow.xml is an illustrative fragment, not a standalone deployment package.
4. Apply API Manager policies for OAuth2/JWT/mTLS as appropriate; authorize audience and scopes on the MuleSoft side independently of Kong.
5. Enable Anypoint Monitoring, structured trace IDs, masking and policy logs; define retries, circuit breaking and connector-specific timeouts.
6. Publish API specifications to Exchange and version them; run contract and integration tests before promotion.
