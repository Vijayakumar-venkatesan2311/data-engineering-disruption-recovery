## Disruption Recovery Intelligence System

### Design Philosophy
This system is designed to support correct decision-making during large scale service disruptions in an online travel agency. When outages happen, different systems send repeated and conflicting updates about the same booking. The goal is not to perfectly reconcile all data, but to prevent incorrect prioritization of customers and revenue exposure when systems are under stress. Instead of trying to make all data perfectly consistent, the focus is on avoiding wrong decisions during high-pressure situations and giving customer support teams information they can trust.

### Data Problems Observed During Disruption
While reviewing the event logs, it became clear that the same booking appears many times in different forms. A single booking ID can generate hundreds of log records because systems retry requests, users repeatedly check flight status, and airline systems send frequent updates. These records reflect what different systems attempted or observed at a specific time, not what finally happened for the customer.

For the same booking, the status often changes multiple times within a short period, moving between delayed, cancelled, and on-time. Although a latest status is visible when events are ordered by time, it cannot be safely treated as the final customer outcome, as additional or conflicting updates may still occur. This makes it unsafe to decide the final booking outcome based only on logs.

Not all log events are tied to a confirmed booking. Some actions, such as logins or flight views, occur before a booking exists, which results in missing booking IDs. These events help explain system activity and customer behavior but should not be treated as booking transactions.

The same booking ID can also appear under multiple airline names. This does not indicate multiple bookings. The booking ID represents a single booking created by the travel agency for one customer. During disruptions, the customer may be rebooked to another airline, or multiple airline systems may send updates related to the same booking. Each airline entry represents an operational update, not a separate business action.

Because of these issues, even after reviewing all events for a booking on a given day, the final customer outcome cannot be determined with confidence from logs alone. The booking snapshot therefore represents the travel agency’s current understanding of customer ownership, tier, and revenue exposure. Treating event logs as the source of truth would inflate counts, misinterpret revenue, and lead to incorrect customer prioritization during outages.

### Why Straightforward Processing Fails

Processing event logs directly during disruptions leads to incorrect conclusions. Counting events by booking or airline exaggerates activity because repeated updates represent retries and system behavior, not customer actions.

Using the latest event to decide booking status is unsafe, as conflicting or late updates can override earlier signals without reflecting the actual customer outcome. Similarly, price values in events represent quotes or estimates and cannot be treated as actual revenue.

Finally, simple aggregation ignores business context. High-value customers with fewer events may require more attention than low-value bookings generating large volumes of log activity. Without considering this, prioritization during outages becomes unreliable.




