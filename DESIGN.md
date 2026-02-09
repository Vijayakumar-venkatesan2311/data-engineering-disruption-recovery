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

### Guiding Principles
**Logs are signals, not final answers**
- Event logs show what different systems reported at a moment in time. They help understand activity and issues, but they are not reliable enough to decide the final customer outcome.

**The booking record is the agency’s truth**
- The booking snapshot reflects what the travel agency currently believes about a booking, including customer ownership, tier, and revenue exposure. This is treated as the stable reference during disruptions.

**One booking always represents one customer**
- A booking ID belongs to the travel agency and identifies a single customer booking. Even if multiple airlines are involved or the booking changes during disruption, it is still the same booking.

**More events do not mean more impact**
- A high number of log events usually indicates retries or system instability, not higher revenue or more customers affected. Business impact is judged using booking value and customer tier, not event count.

**It is better to show uncertainty than give a wrong answer**
- When systems disagree or data is unclear, the design avoids forcing a conclusion. Showing uncertainty is safer than presenting confident but incorrect information during outages.

### Strategy Rationale and Risk Mitigation
Based on the issues seen in the data, the design separates booking state from event activity. The booking snapshot is used to understand customer ownership, tier, and revenue exposure because it represents the travel agency’s current view and contains one record per booking. This avoids inflating revenue or customer impact due to repeated or conflicting log events.

Event logs are used only to understand instability and conflict, such as repeated updates, status changes, or involvement of multiple airlines for the same booking. These signals help identify which bookings may need attention, without treating logs as final truth.

Customer tier is considered when prioritizing bookings, since higher-value customers may require faster attention even if they generate fewer events. When data is unclear or systems disagree, the design avoids forcing a final outcome and instead highlights uncertainty, reducing the risk of confident but incorrect decisions during outages.

### Trade-offs and Limitations
This approach does not attempt to determine the exact final outcome of a booking using event logs alone. Instead, it prioritizes decision safety over completeness. Some insights may arrive later or require manual review, but this avoids misleading customer support teams during high-pressure situations.

The design also accepts that not all conflicting signals can be fully resolved during disruptions. By focusing on stable booking data and surfacing risk rather than forcing conclusions, the system trades speed for accuracy and trustworthiness.



