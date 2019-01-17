-- -----------------------------------------------------
-- Table user
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS user (
  nickname TEXT NOT NULL,
  fullName TEXT NULL,
  email TEXT NULL,
  gender TEXT NULL,
  homeTown TEXT NULL,
  likeCounts INTEGER NULL,
  followingCount INTEGER NULL,
  followerCount INTEGER NULL,
  postCount INTEGER NULL,
  investmentPerspective TEXT NULL,
  verifiedStatus INT NULL,
  registeredTime TEXT NOT NULL,
  PRIMARY KEY (nickname));


-- -----------------------------------------------------
-- Table post
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS post (
  postId TEXT NOT NULL,
  content TEXT NOT NULL,
  posterIsVerify INT NULL,
  numOfComments INTEGER NULL,
  likeCount INTEGER NULL,
  viewCounts INTEGER NULL,
  createdUnixTime TEXT NULL,
  lastUpdated TEXT NULL,
  createdBy TEXT NOT NULL,
  PRIMARY KEY (postId, createdBy),
  FOREIGN KEY (createdBy)
  REFERENCES user (nickname));

CREATE INDEX fk_post_user_idx ON post(createdBy);

-- -----------------------------------------------------
-- Table comment
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  content TEXT NOT NULL,
  createdAt TEXT NULL,
  commenterIsVerify INT NULL,
  likeCounts INTEGER NULL,
  postId TEXT NOT NULL,
  createdBy TEXT NOT NULL,
  FOREIGN KEY (postId)
  REFERENCES post (postId)
  FOREIGN KEY (createdBy)
  REFERENCES user (nickname));

CREATE INDEX fk_comment_post1_idx ON comment(postId);
CREATE INDEX fk_comment_user1_idx ON comment(createdBy);

-- -----------------------------------------------------
-- Table like
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS likes (
  postId TEXT NOT NULL,
  nickname TEXT NOT NULL,
  time TEXT NULL,
  PRIMARY KEY (postId, nickname),
  FOREIGN KEY (postId)
  REFERENCES post (postId)
  FOREIGN KEY (nickname)
  REFERENCES user (nickname));

CREATE INDEX fk_post_has_user_user1_idx ON likes(nickname);
CREATE INDEX fk_post_has_user_post1_idx ON likes(postId);