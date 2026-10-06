import streamlit as st
from ai_engine import analyze_complaint
from database import (
    create_database,
    add_complaint,
    get_complaints,
    update_status
)
import os


# =========================================================
# DATABASE
# =========================================================

create_database()


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Smart City Complaint System",
    page_icon="🏙️",
    layout="wide"
)

st.title("🏙️ Smart City Complaint Management System")


# =========================================================
# CITIZEN SECTION
# =========================================================

st.header("📝 Submit a Complaint")


# Complainant Name
name = st.text_input(
    "👤 Complainant Name",
    placeholder="Example: Rahul Kumar"
)


# Complaint
complaint = st.text_area(
    "Describe your complaint",
    placeholder="Example: There is a large pothole near the college..."
)


# Location
location = st.text_input(
    "📍 Location",
    placeholder="Example: Near ABC College"
)


# Image
image = st.file_uploader(
    "📷 Upload Complaint Image",
    type=["jpg", "jpeg", "png"],
    key="complaint_image"
)


# =========================================================
# SUBMIT COMPLAINT
# =========================================================

if st.button("🚀 Submit Complaint"):

    if name.strip() == "":
        st.warning("⚠️ Please enter your name.")

    elif complaint.strip() == "":
        st.warning("⚠️ Please enter your complaint.")

    else:

        # -------------------------------------------------
        # Save Image
        # -------------------------------------------------

        image_path = ""

        if image is not None:

            os.makedirs("uploads", exist_ok=True)

            image_path = os.path.join(
                "uploads",
                image.name
            )

            with open(image_path, "wb") as f:
                f.write(image.getbuffer())


        # -------------------------------------------------
        # AI Analysis
        # -------------------------------------------------

        with st.spinner("🤖 AI is analyzing your complaint..."):

            result = analyze_complaint(complaint)


        # Make sure result is text
        result = str(result).strip()

        # Remove unwanted pipe characters
        result = result.replace("|", "")

        # Remove accidental Markdown code blocks
        result = result.replace("```text", "")
        result = result.replace("```", "")


        st.success("✅ Complaint analyzed successfully!")


        # -------------------------------------------------
        # Show AI Analysis
        # -------------------------------------------------

        st.subheader("🤖 AI Analysis")

        st.code(
            result,
            language="text"
        )


        st.info(f"👤 Name: {name}")

        if location.strip():

            st.info(
                f"📍 Location: {location}"
            )

        else:

            st.info(
                "📍 Location: Not provided"
            )


        # -------------------------------------------------
        # Default Values
        # -------------------------------------------------

        category = "Other"

        department = "General Department"

        priority = "Medium"

        severity = "Medium"

        summary = result


        # -------------------------------------------------
        # Extract AI Information
        # -------------------------------------------------

        for line in result.splitlines():

            line = line.strip()

            if line.startswith("Category:"):

                category = line.replace(
                    "Category:",
                    "",
                    1
                ).strip()


            elif line.startswith("Department:"):

                department = line.replace(
                    "Department:",
                    "",
                    1
                ).strip()


            elif line.startswith("Priority:"):

                priority = line.replace(
                    "Priority:",
                    "",
                    1
                ).strip()


            elif line.startswith("Severity:"):

                severity = line.replace(
                    "Severity:",
                    "",
                    1
                ).strip()


            elif line.startswith("Summary:"):

                summary = line.replace(
                    "Summary:",
                    "",
                    1
                ).strip()


        # -------------------------------------------------
        # Save Complaint
        # -------------------------------------------------

        add_complaint(
            name,
            complaint,
            location,
            category,
            department,
            priority,
            severity,
            summary,
            image_path
        )


        st.success(
            "💾 Complaint saved to database successfully!"
        )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

st.divider()

st.header("👨‍💼 Admin Dashboard")


# =========================================================
# GET COMPLAINTS
# =========================================================

complaints = get_complaints()


# =========================================================
# CALCULATE STATISTICS
# =========================================================

total = len(complaints)

pending = sum(
    1
    for c in complaints
    if str(c[9] or "Pending") == "Pending"
)

in_progress = sum(
    1
    for c in complaints
    if str(c[9] or "Pending") == "In Progress"
)

resolved = sum(
    1
    for c in complaints
    if str(c[9] or "Pending") == "Resolved"
)


# =========================================================
# STATISTICS DISPLAY
# =========================================================

st.subheader("📊 Complaint Statistics")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.write("📊 **Total Complaints**")

    st.write(f"### {total}")


with col2:

    st.write("⏳ **Pending**")

    st.write(f"### {pending}")


with col3:

    st.write("🔄 **In Progress**")

    st.write(f"### {in_progress}")


with col4:

    st.write("✅ **Resolved**")

    st.write(f"### {resolved}")


# =========================================================
# SEARCH & FILTER
# =========================================================

st.subheader("🔎 Search & Filter")


search = st.text_input(
    "🔍 Search Complaint",
    placeholder="Search by name, complaint, category or location..."
)


filter_status = st.selectbox(
    "📌 Filter by Status",
    [
        "All",
        "Pending",
        "In Progress",
        "Resolved"
    ]
)


# =========================================================
# FILTER COMPLAINTS
# =========================================================

filtered_complaints = []


for c in complaints:

    name_text = str(
        c[1] or ""
    ).lower()

    complaint_text = str(
        c[2] or ""
    ).lower()

    location_text = str(
        c[3] or ""
    ).lower()

    category_text = str(
        c[4] or ""
    ).lower()

    status_text = str(
        c[9] or "Pending"
    )

    search_text = search.lower().strip()


    if (
        search_text in name_text
        or search_text in complaint_text
        or search_text in location_text
        or search_text in category_text
    ):

        if (
            filter_status == "All"
            or status_text == filter_status
        ):

            filtered_complaints.append(c)


complaints = filtered_complaints


# =========================================================
# DISPLAY COMPLAINTS
# =========================================================

if len(complaints) == 0:

    st.info("ℹ️ No complaints found.")


else:

    st.write(
        f"📋 Showing **{len(complaints)}** complaints"
    )


    for complaint_data in complaints:

        # -------------------------------------------------
        # Database Values
        # -------------------------------------------------

        complaint_id = complaint_data[0]

        name = complaint_data[1] or "Not provided"

        complaint_text = complaint_data[2]

        location = complaint_data[3] or "Not provided"

        category = complaint_data[4] or "Other"

        department = (
            complaint_data[5]
            or "General Department"
        )

        priority = (
            complaint_data[6]
            or "Medium"
        )

        severity = (
            complaint_data[7]
            or "Medium"
        )

        summary = (
            complaint_data[8]
            or "No summary available"
        )

        status = (
            complaint_data[9]
            or "Pending"
        )

        image_path = (
            complaint_data[10]
            or ""
        )


        # -------------------------------------------------
        # Complaint Expander
        # -------------------------------------------------

        with st.expander(
            f"Complaint #{complaint_id} — {category} — {status}"
        ):

            st.write(
                "**👤 Complainant Name:**",
                name
            )

            st.write(
                "**📝 Complaint:**",
                complaint_text
            )

            st.write(
                "**📍 Location:**",
                location
            )

            st.write(
                "**🏷️ Category:**",
                category
            )

            st.write(
                "**🏢 Department:**",
                department
            )

            st.write(
                "**⚡ Priority:**",
                priority
            )

            st.write(
                "**📊 Severity:**",
                severity
            )

            st.write(
                "**📄 Summary:**",
                summary
            )

            st.write(
                "**📌 Current Status:**",
                status
            )


            # -------------------------------------------------
            # Complaint Image
            # -------------------------------------------------

            if image_path:

                if os.path.exists(image_path):

                    st.image(
                        image_path,
                        caption="📷 Complaint Image",
                        width=400
                    )

                else:

                    st.warning(
                        "⚠️ Complaint image file not found."
                    )


            # -------------------------------------------------
            # Status Update
            # -------------------------------------------------

            status_options = [
                "Pending",
                "In Progress",
                "Resolved"
            ]


            if status in status_options:

                current_index = (
                    status_options.index(status)
                )

            else:

                current_index = 0


            new_status = st.selectbox(
                "🔄 Update Status",
                status_options,
                index=current_index,
                key=f"status_{complaint_id}"
            )


            if st.button(
                "💾 Update Status",
                key=f"update_{complaint_id}"
            ):

                update_status(
                    complaint_id,
                    new_status
                )

                st.success(
                    "✅ Status updated successfully!"
                )

                st.rerun()