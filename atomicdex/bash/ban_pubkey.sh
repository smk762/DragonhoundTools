source userpass
curl --url "http://127.0.0.1:7783" --data "{
  \"userpass\": \"$userpass\",
  \"method\": \"ban_pubkey\",
  \"pubkey\": \"2cd3021a2197361fb70b862c412bc8e44cff6951fa1de45ceabfdd9b4c520420\",
  \"reason\": \"testing\"
}"
