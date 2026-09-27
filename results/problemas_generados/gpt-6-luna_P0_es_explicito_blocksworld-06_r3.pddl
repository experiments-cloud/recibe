(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
  )
  (:init
    (ontable b)
    (ontable c)
    (on a c)
    (on d a)
    (on e b)
    (on f e)
    (clear d)
    (clear f)
    (handempty)
  )
  (:goal
    (and
      (on a e)
      (on b a)
      (on c b)
      (on e f)
      (on f d)
    )
  )
)
