from config.supabase_config import supabase

class SupabaseService:
    @staticmethod
    def get_table_data(table):
        try:
            if table == "onboarding":
                # No join needed for onboarding
                response = supabase.from_(table).select("*").execute()
                data = [
                    {**row, "full_name": row.get("full_name", "")}
                    for row in response.data
                ]
                print(f"Fetched {len(data)} rows from {table}")
            else:
                try:
                    # Try explicit join with foreign key
                    response = supabase.from_(table).select("*, onboarding!agent(full_name)").execute()
                    data = [
                        {**row, "full_name": row["onboarding"]["full_name"] if row.get("onboarding") and row["onboarding"].get("full_name") else ""}
                        for row in response.data
                    ]
                    print(f"Fetched {len(data)} rows from {table} with join")
                except Exception as join_error:
                    print(f"Join failed for {table}: {str(join_error)}")
                    # Fallback: Fetch raw table data without join
                    response = supabase.from_(table).select("*").execute()
                    data = [
                        {**row, "full_name": ""}  # Add empty full_name for consistency
                        for row in response.data
                    ]
                    print(f"Fallback: Fetched {len(data)} rows from {table} without join")
            if not data:
                print(f"No data returned for {table}. Check table data or schema.")
            return data
        except Exception as e:
            print(f"Error fetching {table} data: {str(e)}")
            return []

    @staticmethod
    def get_table_columns(table):
        columns = {
            "agents": ["agent", "total_call_attempt", "unique_dialed", "connected", "total_call_duration", "not_connected", "call_back_later", "time_clock_hrs", "status", "full_name"],
            "onboarding": ["id", "timestamp", "email_address", "full_name", "phone_number", "email_id", "job_position", "google_drive_link_interview", "wa_reminder", "results", "salary", "doj", "exit_date", "days_left", "agent"],
            "agent_hourly_metrics": ["id", "agent", "total_call_attempt", "unique_dialed", "connected", "total_call_duration", "not_connected", "call_back_later", "hour_timestamp", "full_name"],
            "calls": ["call_id", "agent", "duration", "phone", "connected_status", "call_back_status", "date_time", "full_name"],
            "key_assignment": ["agent", "business_developer_associate", "date_of_exit", "date_of_joining", "assignable", "full_name"],
            "archives": ["agent", "full_name", "date_of_exit", "total_talktime","no_of_calls","attendance_count"],
        }
        return columns.get(table, [])