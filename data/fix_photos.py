#!/usr/bin/env python3
"""Fix the off-by-one photo mapping in delta_fellows.json.

The original scrape grabbed the Delta Institute logo as the first image,
pushing every photo one position forward. The correct mapping (from DOM scraping):
- Fellow[0] should get photo that was assigned to Fellow[1]
- Fellow[1] should get photo that was assigned to Fellow[2]
- ... and so on
- Fellow[143] (last) needs its correct photo from the DOM data
"""
import json

with open('/Users/vansh/Brainstorming/delta_fellows.json') as f:
    data = json.load(f)

# The correct file IDs scraped from the live DOM via Chrome
correct_file_ids = {
    "Alexi Gladstone": "qYNLkwcNeWIQl2HqE9ItAevKwOs.jpeg",
    "Luke Melas-Kyriazi": "LGYweg5qQ7v3bzw3m9BDl1e4Q.jpeg",
    "Rohan Pandey": "0fysHtiazR6b8HFhQiPH0ayeh8.jpeg",
    "Eric Han": "J7zwNE27BQm4L0Dj26gjnD7b3w.jpeg",
    "Bo Peng": "H0nAleqJhkDdK7JVW9yxDoB4ToA.png",
    "Lisa Dunlap": "DoN6F9P8x6ZsaND7O8qB2sfcuQ.png",
    "Kshitij Sodani": "uoJWgrXxUrgr9vbupFv2TlRpAA.png",
    "Emily Han": "sEC7P0OtcnZY7ZKRtp3kQJfJRk.jpeg",
    "Alex Zhang": "536Xwb9OvrGfkPCE6eI2foLLtc.jpeg",
    "Laker Newhouse": "biEsr5HgouB9oRKkiEdgQqW0ADQ.jpeg",
    "Stuart Sul": "txTQzmJWfjRA0CiwElyUdxO1UY.jpeg",
    "Haneul Shin": "NhlxGO01WxFmhFCuqsoxBH5QZQg.jpeg",
    "Cynthia Chen": "3v9QaMlQd64pyj5Uh5RJIuJzw.jpeg",
    "John Yang": "GHS37UokIZuSg1uXILESMtpQ9hI.png",
    "Dan Biderman": "Mj8qMXqwpC4ifBxQV0lnXCMRtY.jpeg",
    "Kevin Lu": "Rd3pMt6u5gTudwuOu1o8z5lFyl4.jpeg",
    "Ronak Malde": "e4WRq3Rrsv9pPXcyfQQ426zHBs.jpeg",
    "Avanika Narayan": "vzQFa48zFWCJvRrqJUaKz3OFZA.jpeg",
    "Grace Li": "Pi1WpFR85iAAX6AF70q9b4SQ4i0.png",
    "Gashon Hussein": "YQaM8K49TZ9wCV68gxWB4A0lRBk.jpeg",
    "Jayesh Singla": "I1K7DEyWJJ7wbQF2qr0zGjorRns.jpeg",
    "Welton Wang": "4RSaFVWVfqBWD5s0OT1Bz9K0.jpeg",
    "Rohan Kalahasty": "0KCPw1bSA61jIcvNGBVfqjBMo.jpeg",
    "Amy Jin": "fVPEVfPrGxqQq28LjEjTnVF1Bo.jpeg",
    "Zeyneb Kaya": "rjxZPL5PiGvyqMiDhKdKoddRTI.jpeg",
    "Nikita Mounier": "fv6fShHaZUXEwfW8hx5dZNNYWrM.png",
    "Simon Guo": "g9FqGkxbHtIqlXwLvz2ndSZmc.jpeg",
    "Oam Patel": "gm4ItH6KDJsPfCPBW4cF8dJ3dUc.jpeg",
    "Archer Wang": "hPl9PcnMnTlAIWUkPkJQlL4g.jpeg",
    "Hannah Gao": "MiV8kCTGWr6T1oqe5jx4L44gVk.jpeg",
    "Sally Zhu": "JBmn9iqhKIqJwwflrR9HQWK6Y.jpeg",
    "Ayush Alag": "rr8g02Tyu6EjnfswRqhFD8dBw.jpeg",
    "Brian Huang": "8bxQTOXOD0sCp23XBk39LxKU.jpeg",
    "Aarav Wattal": "YPj6ZZAkAAbSwEBpLjJVHoM.jpeg",
    "Thijs Simonian": "3D12QBmqHuPb5FTkKDzuoKo6k.jpeg",
    "Grace Luo": "J3hfvmVEFpSZA2rfaEdOsYKF2ss.jpeg",
    "Nina Boord": "KUJlBkTJNJHSQnXiQlBVCvyYA.jpeg",
    "Alex Gu": "rCELlkXcfhBk09bTyv12s2hHu3s.jpeg",
    "Sachit Menon": "8mVqkKzfxAp3t0PxE0AHVqS5r0.png",
    "Xingjian Bai": "xV4jylJcGlMXrqhZvOJjOTz5aI.jpeg",
    "Joe Li": "YBdVUcl3K54B4VgxZWMGVZlz4RE.jpeg",
    "Gauri Gupta": "lnTcxQqNWp7DdFchh7cOT6g.jpeg",
    "Mihika Dusad": "H16kddVi1s29tGPyA8yI8bwzCnY.jpeg",
    "Etash Guha": "FCnYfGk3wMmOPFxpnN1FV2jk5UU.jpeg",
    "Stephen McAleer": "VxBcELClmAlFtR5jX7GYxoqJE.jpeg",
    "Elijah Kurien": "jQWnkE7SpYlsdfR6m6DScYS0.jpeg",
    "James Chen": "i37yXagEFT1GKNuXvlwTzFdKkpA.jpeg",
    "Lillian Sun": "m2G2VBXzuoGaJJ4VbHGrWRBKuk.jpeg",
    "Bonnie Li": "vW2WJT7k3U7V6h1Kf0CJwDYIVQg.jpeg",
    "Spruce Campbell": "m6LrGdW3Qu8Shu7F5lnhdR9jv0.jpeg",
    "Khush Gupta": "UtfyF47qaPQdyyHAIPikV74qDo.jpeg",
    "Leonard Tang": "5vD0jRDiAL8fA2fDZ20AR8LQQJI.jpeg",
    "Sai Konkimalla": "WkfCffl2tqGGNKKvHaDq4jfP4.jpeg",
    "Sonya Jin": "L3AuYA3tDLhLQ0iy4WbcK0QJvFQ.jpeg",
    "Niloofar Mireshghallah": "T2k3IvKmaNNYnYdoGQ6gaNv8WbE.jpeg",
    "Patrick Wang": "PvzkD7x3mjC7bodzlLUfiMDMdw.jpeg",
    "Zeeshan Patel": "8D8dsByqdMoWy7nsdxpdz1a9kU.jpeg",
    "Zirui (Colin) Wang": "9lh4HPNUaQoCeUQ0b3Vemkp50.jpeg",
    "Isaac Fung": "36fI9JLlJQXuDgqVMa00a3Eq9uY.jpeg",
    "Ally Nakamura": "yRBsAJlL7qCsIlok2MfIhyR4fs.jpeg",
    "Brooke Joseph": "FTtwveVLwUdstqXIedRjhweUG1k.jpg",
    "Alex Shan": "DpkWCmAKZpiII5dvNvQY85U.jpeg",
    "Rohan Tibrewal": "TqwJMGyiLt8YVmwpFXbTZCAtaQ.jpeg",
    "Fan-Yun Sun": "63R0JLO2MEtRY1poDvz7r88PZzU.jpeg",
    "Suvansh Sanjeev": "jdGv9eRzzpH4qbc9wt4S592EpX0.jpeg",
    "Grace Lam": "BbtQBexcyGPa7RMtM52amZd8Lw.jpeg",
    "Kavya Anbarasu": "P4TD57OWIb3mvuAlTnHemSlIt0.jpeg",
    "Neil Kale": "zliPES4SDC8djJeAgpyg6xhnp60.jpeg",
    "Stephen Xie": "Dzhx7e0TfzTiFNiBmRrRdfLRRc.jpeg",
    "Isaac Ong": "UwutOHLPsSkBLlXSBguGqO4xqgk.jpeg",
    "Eric Zhang": "rPd6XKvQnqTP52ofV1nWEWUGtY.jpeg",
    "Helen Wang": "hVxTyJW9TtQPcIlg9dqGMDkts.jpeg",
    "Sandra Yang": "u6s4eB3FH9IFzHGGvNQW0cC3U.jpeg",
    "Kevin Wang": "V86XPVQAA2VgHzJwC6KDo1QE.jpeg",
    "Damian Ho": "X8p1Csl98Ek1R97LNpZfGiAkE.jpeg",
    "Sid Bharthulwar": "vLK7bQlqPMsQHYDUNMdH4uFLts.jpeg",
    "Hima Tammineedi": "pHh6UuPFX8G7WfIVZsNqHU.jpeg",
    "Serena Ge": "i9GRvRupkHUlp5Ns3UQqWw33oSE.jpeg",
    "Sijun Tan": "Q8XY68vGpTuJbf2r6VJSxOOk.jpeg",
    "Vineet Edupuganti": "UcDNiYgGnZOCRhqILFPgHkss1w.jpeg",
    "Mingyang Deng": "eMC55K2d9MHQV62mcrbbh04fqo.jpeg",
    "Preston Fu": "lE9m5FIqDGfFIqLOOI2Vug9PiRc.jpeg",
    "Karthik Balaji Ganesh": "Wsa6qr6MwFqZv0rcYqGjcWLhH8.jpeg",
    "Devvrit Khatri": "6L3lF3xCebz8XRqhJWfMXLqaHs.jpeg",
    "Hersh Godse": "4W7ULO5Dz7AJDmTqhKFKOKYgMwk.jpeg",
    "Shobhit Agarwal": "LVLxeSQVBJz9HjsWMN7TRpIJTsM.jpeg",
    "Andrew Ma": "IqvNJlf44OGSJ7VVjPgpNH5gOJA.jpeg",
    "Rajan Agarwal": "VyFYmF5HZbTOC3JwEF4TqWPk.jpeg",
    "Ian Moore": "P7nz4Ky4KPYJh4xnrKE1f0oWc.jpeg",
    "Fan Pu Zeng": "LfRwpSEMCRaNLKnZm6BUW6rFQ.png",
    "Abhay Venkatesh": "UtKjF3N44m4dHO9IXdoZhz3UHA.jpeg",
    "Bolaji Makinde": "OFv6Lh1XwVFAqrH8tIyhewlBOM.jpeg",
    "Michael Wornow": "X4a8XfKVqCk6sHLHjYy1EAfjH8.jpeg",
    "Yusuf Ozuysal": "8XFcbkb0UMw9b11rlrR3NKdDmfo.jpeg",
    "Raj Palleti": "hWjFf9eBMfrFNXhqTawf6WOg8.jpeg",
    "Aadi Nashikkar": "y54H36QhtGKjb1bVFjhfTl3jSGg.jpeg",
    "Nate Marquez": "7rcxNTKWYMU7sVqGdHOt5OmVOiE.jpeg",
    "Allen Nie": "SfNdkAqF16MRSqlmnnvtxqsJMM.jpeg",
    "Aditya Gupta": "tIfJbPDVjkKddMaZRdfjeSF238.jpg",
    "Ameen Patel": "Ptr8p8lW9QbfDeRcLW74b04Gss.jpeg",
    "Kartik Srinivas": "K6EiWvqYzdHwpcAZhOEfYbclcbA.jpeg",
    "Jeffrey Ma": "WFLUSuv8JMrVzfrs1ZWZhgfeL0I.jpeg",
    "David Krajewski": "7hglBLj8WLP0Em1fFGDUMZKrwG4.jpeg",
    "Ishaan Javali": "mXEADeqYZhT43tRezjQXYOhwcec.jpeg",
    "Kirill Acharya": "wK4idRa5glr3BFWAEZBrR32XzZQ.jpg",
    "Ari Webb": "RpovEtUY7RKHYwovAH27V6Sn4tE.jpeg",
    "Charles Ding": "cuRbzg0rXNI41PudJ29N4DpMSM.jpeg",
    "Aakash Mishra": "8JAqDNgV1zmuzAG1sGjCR4y2as0.jpeg",
    "Maxwell Jones": "1xuQ2ZwCEEQYI9zbkV1MRECxVoQ.jpeg",
    "Jonathan Mengedoht": "EeyWwO66KnUpmBRtkQPPmn8r80Q.jpeg",
    "Jon Saad-Falcon": "02dvAFUhoip37ccjhnRC1v0PE.jpeg",
    "Rohin Manvi": "zp4Rnq73lghoyHV7s0PLi1jPLOo.jpeg",
    "Hima Tammineedi": "X2XdnX2WUwo0AXezHgqVTlxIXYo.jpeg",
    "Utkarsh Priyam": "RZUnaOVv3HVinFxLmrlDmj1VbJM.jpeg",
    "Yassine Kachrad": "fB5A451dg0Fqu0FY37d4GH74I.png",
    "Samarth Goel": "ln7w2vzWWPWjG04Ma3dF8jZ7Ug.jpeg",
    "Taarush Grover": "SZQ81BVWuJTNdDaPL5PADU7wU4.jpeg",
    "James Liu": "26olZuUfPzIW8RPIkQf6QPH9hNQ.jpeg",
    "Sudarshan Nambiar": "MU7AZdlke06FCrJLjnLZBNBB8.jpeg",
    "Parsa Idehpour": "BkGYlmrm98jk9GCaO8UdIo86Z8M.jpeg",
    "Niklas Muennighoff": "VcwNMXKUdlmVjZ4LxNuqPZHRVU.jpeg",
    "Rong Ye": "PZdpAPfWXNbpwOF0JZ4BUbYM.jpeg",
    "Jaeyeon Kim": "TdJHCTdC4q17FDo8S7cVPl1u2Q.jpeg",
    "Harsh Shah": "6QI5f1O7nMrH3xKPqg9u9IQ.jpeg",
    "Adam Lee": "P0RNJmz5cN6G8E8OUWdGUWrK6g.jpeg",
    "Michael Elabd": "Gn2LI7p5IRLAE75N8LtHHp3LS0c.jpeg",
    "Raj Mehta": "oaLt10dRPGXfDFp3nCfGhLnlR0.jpeg",
    "John Rho": "FPLK6lqNJvzQlTEGPIXzGWMHYuk.jpeg",
    "Zhening Li": "F26cj36UO7PzQd9xuhqFewKiAQ.jpeg",
    "Matthew Yang": "Ej6pKZbMjxLOLPbHlW4aA1hgHao.jpeg",
    "Jerry Zhou": "3NWYUJdwfL17lgaGF4kcMpOjjG4.jpeg",
    "Seaver Dahlgren": "c5IIajfMc3X8NMqpbWKbYJEy33Y.jpeg",
    "Jacob Zietek": "DRLiW4eMc2xC2RYwCuMCsyKI.jpeg",
    "Joseph Melkonian": "oL4WKTd23LZCgHewH7sItaIYNE.jpeg",
    "Vincent Tombari": "aJGUoAvLPMrswlE7xYkT3UEyqfA.jpeg",
    "Chenglei Si": "sFo4TGpNjlNdJ4eSNMaHsA7jEKg.jpeg",
    "Shreyas Sreenivas": "LjgPr32WcspEvLGXw7Z8qSMr4Rs.jpeg",
    "Sid Bharthulwar": "1eNXv5TaJG3A8bO2NKZmUOl1Xk.jpeg",
    "Lawrence Jang": "3FfpUKrqvJkPDPaxJWuQ2DsY.jpeg",
}

# Update each fellow's photo
base_url = "https://framerusercontent.com/images/"
fixed = 0
for fellow in data:
    name = fellow['name']
    if name in correct_file_ids:
        fid = correct_file_ids[name]
        # Construct URL with reasonable default sizing
        ext = fid.split('.')[-1]
        new_url = f"{base_url}{fid}?width=400&height=400"
        if fellow['photo'] != new_url:
            old_fid = fellow['photo'].split('images/')[-1].split('?')[0] if fellow['photo'] else 'NONE'
            fellow['photo'] = new_url
            fixed += 1

with open('/Users/vansh/Brainstorming/delta_fellows.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed {fixed} photos out of {len(data)} fellows")
