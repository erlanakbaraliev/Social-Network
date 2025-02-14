document.addEventListener("DOMContentLoaded", ()=>{
    setupNavigation()

    loadView("#allpostsView")
    // setupAllPostsPagination(): api call to the 1st pagea and renders it. Adds pagination to the 'next' 'previous' buttons. 
    // Each time a button is pressed api call to the next/previous page is made and rendered.
    // This method needs to be called only once as it has a field that keeps track of the current page by incrementing and decrementing
    // also because add an event listener to the 'next', 'previous' buttons is enough
    setupAllPostsPagination()
})

function setupNavigation() {
    const navigation = {
      '#allposts': () => {
        loadView('#allpostsView')
        
        displayPage(1)
    },
      '#profile': () => {
        loadView('#profileView')

        const profileButton = document.querySelector('#profile');
        const username = profileButton ? profileButton.dataset.username : null;
        if(username) {
            setupProfilePagination(username)
        }
    },
      '#followed': () => {
        loadView("#followedView")

        const profileButton = document.querySelector('#profile');
        const username = profileButton.dataset.username

        setupFollowedPagination(username)
    },  
      '#followers': () => {
        loadView("#followersView")
    },
      '#login': () => {
        loadView("#loginView")
      }
    };
  
    Object.entries(navigation).forEach(([selector, handlers]) => {
      const viewButton = document.querySelector(selector);
      if (viewButton) { 
        viewButton.addEventListener('click', (event) => {
          event.preventDefault();
          handlers()
        });
      }
    });
}

function loadView(viewId) {
    ['#allpostsView', '#profileView','#followedView', "#followersView", "#loginView"].forEach(id => {
        const div = document.querySelector(id)
        if(div) {
            div.style.display = id === viewId ? 'block' : 'none';
        }
      });
}

// --------------------------------------------------------------------------
// renderPosts(posts, divID) is used by Main page (allPosts) and Profile page views

function renderPosts(posts, divID) {
    const postsDiv = document.querySelector(`${divID}`);
    postsDiv.innerHTML = "";  // Clear current posts

    posts.forEach(post => {
        const postEl = document.createElement("div");
        postEl.className = "card";
        postEl.innerHTML = `
            <div class="card-body">
                <h4 class="card-title">@${post.user}</h4>
                <p class="card-text">${post.content.replace(/\n/g, '<br>')}</p>
                <p class="card-text"><small class="text-muted">${post.timedate}</small></p>
            </div>
        `;
        postsDiv.appendChild(postEl);
    });
}

// --------------------------------------------------------------------------
// Main page

// called only once
function setupAllPostsPagination() {
    const prevButton = document.querySelector("#all-prev");
    const nextButton = document.querySelector("#all-next");
    let pageNumber = 1;

    displayPage(pageNumber);

    prevButton.addEventListener('click', (event) => {
        event.preventDefault();
        if (pageNumber > 1) {
            pageNumber--;
            displayPage(pageNumber);
        }
    });

    nextButton.addEventListener('click', (event) => {
        event.preventDefault();
        pageNumber++;
        displayPage(pageNumber);
    });
}

// called each time 'next' or 'previous' buttons are clicked
function displayPage(pageID) {
    fetch(`page/${pageID}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.log(`PageID: ${pageID}`)
            console.error(data.error);
            return;
        }
        renderPosts(data.posts, "#posts");

        const prevButton = document.querySelector("#all-prev");
        const nextButton = document.querySelector("#all-next");

        prevButton.disabled = !data.has_previous;
        nextButton.disabled = !data.has_next;
    })
    .catch(error => console.error("Error fetching page:", error));
}

// --------------------------------------------------------------------------
// Profile page
function setupProfilePagination(username) {
    const prevButton = document.querySelector("#profile-prev");
    const nextButton = document.querySelector("#profile-next");
    let profilePageNumber = 1;
    
    displayProfile(username, profilePageNumber);

    prevButton.addEventListener('click', (event) => {
        event.preventDefault();
        if (profilePageNumber > 1) {
            profilePageNumber--;
            displayProfile(username, profilePageNumber);
        }
    });

    nextButton.addEventListener('click', (event) => {
        event.preventDefault();
        profilePageNumber++;
        displayProfile(username, profilePageNumber);
    });
}

function displayProfile(username, page=1) {
    fetch(`profile/${username}?page=${page}`)
    .then(response => response.json())
    .then(data => {
        renderPosts(data.posts, "#profilePosts");
        renderFollow(data.followed.length, data.followers.length)
        
        const prevButton = document.querySelector("#profile-prev");
        const nextButton = document.querySelector("#profile-next");
        prevButton.disabled = !data.has_previous;
        nextButton.disabled = !data.has_next;
    })
    .catch(error => console.error("Error fetching profile:", error));
}

function renderFollow(followedCount, followersCount) {
    document.querySelector("#followed").textContent = `Followed: ${followedCount}`
    document.querySelector("#followers").textContent = `Followers: ${followersCount}`
}

// --------------------------------------------------------------------------
// Folowed and Followers page

function setupFollowedPagination(username) {
    displayFollowed(username)
}

function displayFollowed(username) {
    fetch(`profile/${username}`)
    .then(response => response.json())
    .then(data => {
        renderFollows(data.followed, "#followedPosts")
    })
}

function renderFollows(posts, divID) {
    const postsDiv = document.querySelector(`${divID}`);
    postsDiv.innerHTML = "";

    // each follower/following is a post
    if(divID === "#followedPosts") {
        posts.forEach(post => {
            const postEl = document.createElement("div");
            postEl.className = "card";
    
            postEl.innerHTML = `
                <div class="card-body">
                    <h4 class="card-title">@${ post.followed }</h4>
                </div>
            `;
            
            postsDiv.appendChild(postEl);
        });
    }
    else {
        posts.forEach(post => {
            const postEl = document.createElement("div");
            postEl.className = "card";
    
            postEl.innerHTML = `
                <div class="card-body">
                    <h4 class="card-title">@${ post.followers }</h4>
                </div>
            `;
            
            postsDiv.appendChild(postEl);
        });
    }
}