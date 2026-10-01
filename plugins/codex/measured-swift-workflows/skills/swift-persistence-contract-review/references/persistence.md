# Persistence review contract

Map model/container identity, actor/context owner and write authorization. SwiftData does not imply CloudKit; inspect configuration and the actual sync protocol. Review stable IDs, relationships, defaults, enum storage, tombstones and retries against retained data. Do not copy constraints from a different storage system. Propose migration tests with synthetic old/new records; execution requires separate authority.

Authority: [Persistence review contract](https://developer.apple.com/documentation/swiftdata/modelactor). Documentation informs correctness; it is not evidence that this workflow ran successfully in an installed client.
