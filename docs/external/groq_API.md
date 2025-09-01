GROQ-JS API (excerpt)

Source: sanity-io/groq-js `API.md` (public API)

parse(input: string, options?: ParserOptions) -> ExprNode

- ParseOptions:
  - params?: Record<string, unknown>
  - mode?: 'normal' | 'delta'

Throws: GroqSyntaxError { position: number, name: 'GroqSyntaxError' }

evaluate(node: ExprNode, options?: EvaluateOptions) -> Promise<any>

- EvaluateOptions (useful fields):
  - root?: any        # value available as `@`
  - dataset?: any     # value available as `*`
  - params?: Record<string, unknown>
  - timestamp?: Date  # timestamp used for now()
  - identity?: string
  - before?: any       # delta-mode
  - after?: any        # delta-mode
  - sanity?: { projectId: string; dataset: string }

typeEvaluate(ast: ExprNode, schema: SchemaType) -> TypeNode

Usage pattern (example):

```javascript
import { parse, evaluate } from 'groq-js'

const tree = parse("*[_type == 'user']{name}")
const value = await evaluate(tree, { dataset })
const result = await value.get()
```

Error handling:
- Catch `GroqSyntaxError` to return a 400 with `position` and `message` for malformed queries.

Notes for integration:
- Expose an endpoint POST /query that accepts { query: string, params?: object }.
- Call `parse`, then `evaluate`, and return the evaluated result (or error details on parse failures).
- Consider adding a thin adapter that maps your DB retrieval into the `dataset` parameter.
